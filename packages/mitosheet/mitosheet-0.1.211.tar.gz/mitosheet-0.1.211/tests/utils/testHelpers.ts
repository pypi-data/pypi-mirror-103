// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

/*
    This file contains all the helpers for setting up
    and running different mitosheet tests.  
*/

import { Selector} from 'testcafe';
import { testUser } from './roles';
import { 
    selectKernelButton,
    fileTab,
    fileTabNew,
    fileTabNewNotebook,
    getActiveElement,
} from './selectors';

import { exception } from 'console';
import { LOCAL_TEST } from '../config';
import { tourCloseButton } from './tourHelpers';


/* 
    Setup is the a function that is responsible for setting up 
    the testing notebook. 

    After this function runs, we assume that the testing enviornment
    is "setup" for the tests (e.g. you can call tryTest and the test
    will run).
*/
export async function setup(t: TestController): Promise<void> {
    if (!LOCAL_TEST) {
        await t.useRole(testUser)
        await t.wait(25000) // wait 25 seconds            
    }

    // We sign up to create an account
    await clearAllCreateNewNotebook(t, 'import mitosheet\nimport pandas as pd\ndf=pd.DataFrame({"A":[123]})\nmitosheet.sheet(df)');
    await signIn(t, true);
    await t.pressKey('ctrl+s');
}

/*
    Checks if there is a modal open with a input field and tries to sign in
    if it exists. 

    If closeTour is true, closes the tour that pops up if the user.

    If this function fails, does not error - as the signup input
    exists depending on global state - if the user has signed in 
    before.
*/
async function signIn(t: TestController, closeTour: boolean): Promise<void> {
    // Sign in if the user is required to
    try {
        // if the signup modal appears, click on it and sign in
        await t
            // We wait for a few seconds for it to render, the first time
            .wait(10000)
            .typeText(
                Selector('input.input'),
                'testcafe@test.com'
            )
            // then submit by hitting the enter button
            .pressKey('enter')
            // Then advance through the privacy policy
            .pressKey('enter')
            // Then, continue without selecting any intended behavior
            .pressKey('enter')
    } catch (e) {
        // We don't care if the login works, so we suppress this error
    }

    // Note: we don't do this in the same try catch as the above, so
    // we make sure we get the pesky tour if it's around. We create a bunch 
    // of try catches so that the we can close all of the tours
    try {
        // Then, close the tour, if it pops up, and we want to close it
        if (closeTour) {
            await t.click(tourCloseButton);
        }
    } catch (e) {
        // Again, we don't care if it works, so we suppress the error
    }

    // Clicking the close button takes you to the tutorial tour, so we close it
    try {
        // Then, close the tour, if it pops up, and we want to close it
        if (closeTour) {
            await t.click(tourCloseButton);
        }
    } catch (e) {
        // Again, we don't care if it works, so we suppress the error
    }
}


/*
    Assumes there is an open notebook, where the content can be deleted and replaced.

    All content is deleted, the top cell is filled with cellText, and the cell is run.
*/
export async function fillCurrentNotebook(t: TestController, cellText: string): Promise<void> {

    const cellInputBox = Selector('div.jp-InputPrompt')

    await t.wait(10000);
    const inputCount = await cellInputBox.count;

    await t.pressKey('esc')

    for (let i = 0; i < inputCount; i++) {
        await t.pressKey('d').pressKey('d');
    }

    await t
        .pressKey('enter')
        // Then, we create a mito notebook
        .typeText(
            // By default, the first cell is focused on
            getActiveElement(), 
            cellText
        )
        .pressKey('shift+enter')
}


/* 
    Deletes all notebooks in the current folder.
*/
export async function deleteAllNotebooks(t: TestController, failOnFailure?: boolean): Promise<void> {
    const notebookCount = await Selector('ul.jp-DirListing-content').child('li').count

    if (notebookCount === 0) {
        return;
    }
    
    try {
        // First, click the first notebook
        const firstNotebook = Selector('ul.jp-DirListing-content').child('li').nth(0)
        await t.click(firstNotebook)

        // Then, shift click the last notebook
        const last = Selector('ul.jp-DirListing-content').child('li').nth(notebookCount - 1)
        await t.click(last, {modifiers: {shift: true}})

        // Then, delete them all!
        const deleteModalButton = Selector('div.jp-Dialog-buttonLabel')
            .withExactText('Delete')

        await t
            .rightClick(firstNotebook)
            .pressKey('d')
            .click(deleteModalButton)
    } catch (e) {
        if (failOnFailure) {
            throw exception('Failed to delete notebooks!');
        }
        console.log("Failed deleting all notebooks")
    }
}

/* 
    A function for resetting everything, it deletes all existing notebooks,
    creates a new notebook, and fills it with the cellText passed, before
    running the cell
*/
export async function clearAllCreateNewNotebook(t: TestController, cellText: string) {
    // First, we check if there is currently a select kernel modal (which there is sometimes
    // when a notebook fails to be deleted, for some reason. If there is, we click it, as many
    // times as it pops up
    try {
        // Keep clicking kernel buttons, as long as they are there!
        while (!(await selectKernelButton.exists)) {
            await t.click(selectKernelButton)
        }
    } catch (e) {
        // We don't care if this fails... it only needs to happen it when does...
    }

    // Then, we delete all the notebooks there are
    await deleteAllNotebooks(t);

    // Then, make a new notebook
    await t
        .click(fileTab)
        .hover(fileTabNew)
        .click(fileTabNewNotebook)

    // Then, we try to select a kernel (this popup only appears sometimes), 
    // which is why we don't necessarily _need_ to click it
    try {
        await t.click(selectKernelButton)
    } catch (e) {
        console.log("No need to select kernel.")
    }

    await fillCurrentNotebook(t, cellText);
}


/*
    This is a helper function that should wrap every test. It is responsible
    for actually running the tests, and does so by:
    1. Assuming that setup has been called, and trying to run a test.
    2. If this fails, deleting all notebooks and resetting up, to try to 
       rerun the test
       
    It tries to run the test 4 times, with an increasing delay between them, four times. 
    This is to ensure any testcafe tests that randomly fail can be avoided. 
    
    As the Mito app doesn't have much concurreny or non-determinstic behavior, 
    tests only passing some of the time has been a function of testing issues.

    Note that if closeTour is not passed, it defaults to true.
*/
export async function tryTest(t: TestController, cellText: string, test: (t: TestController) => Promise<void>, closeTour?: boolean): Promise<void> {
    let failed = false;

    if (closeTour === undefined) {
        closeTour = true;
    }

    // First, fill up the window
    await t.maximizeWindow();
    
    try {
        // Sign we should we set up, we can just fill the current notebook
        await fillCurrentNotebook(t, cellText);
        // Then, we run the test
        await test(t);
    } catch (e) {
        console.error(e);
        failed = true;
    }

    // Return if we have not failed
    if (!failed) {
        return;
    } 
    
    failed = false;
    for (let i = 0; i < 3; i++) {
        try {
            console.log(`Try ${i + 1}, running with timeout ${5000}`)
            await t.wait(5000);
            await clearAllCreateNewNotebook(t, cellText);
            await signIn(t, closeTour)
            await test(t);
        } catch (e) {
            console.log(`Failed try ${i + 1} with error`);
            console.error(e);
            failed = true;
        }

        if (!failed) {
            return;
        }
    }

    console.log("Waiting 60 seconds before last try")
    await t.wait(60000);

    // Don't wrap the last one, because we want to fail if this fails!
    console.log("Running last test")
    await clearAllCreateNewNotebook(t, cellText);
    await signIn(t, closeTour)
    await test(t);
}