// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

/*
    Contains all useful selectors and helpers for repeating an analysis.
*/

import { Selector } from 'testcafe';
import { modalAdvanceButtonSelector } from './allModals';
import { DELETE_PRESS_KEYS_STRING } from './helpers';
import { simpleImportSelect, simpleImportSelectOption } from './importHelpers'
import { getActiveElement } from './selectors';


export const repeatAnalysisButton = Selector('p')
    .withText('Replay')
    .parent()

/* 
    Helper function that returns a selector for the Apply this Analysis Button
*/
export const getReplayAnalysisButton = (): Selector => {
    return Selector('div.custom-dropdown')
        .child('div')
        .withText('Apply this Analysis')
}

/* 
    Helper function that returns a selector for the saved analysis name. Double click it to rename
*/
export const getSavedAnalysisNameDiv = (savedAnalysisName: string): Selector => {
    return Selector('div.saved-analysis-card')
        .child('div')
        .withExactText(savedAnalysisName)
}

/* 
    Helper function that returns a selector for a saved analysis in the
    saved analysis list
*/
export const getSavedAnalysisDropdown = (savedAnalysisName: string): Selector => {    
    return Selector('div.saved-analysis-card')
        .child('div')
        .withExactText(savedAnalysisName)
        .parent()
        .find('div.saved-analysis-card-dropdown-div')
}

/* 
    Helper function that returns a selector for the Delete this Analysis Button
*/
export const getDeleteAnalysisButton = (): Selector => {
    return Selector('div.custom-dropdown')
        .child('div')
        .withText('Delete this Analysis')
}

/*
    Repeats the analysis with the given name
*/
export async function repeatAnalysis(t: TestController, analysisName: string): Promise<void> {
    await t
        .click(repeatAnalysisButton)
        .click(getSavedAnalysisDropdown(analysisName))
        .click(getReplayAnalysisButton())
}

/* 
    Deletes the saved analysis with the given name
*/
export async function deleteSavedAnalysis(t: TestController, analysisName: string): Promise<void> {
    await t
        .click(repeatAnalysisButton)
        .click(getSavedAnalysisDropdown(analysisName))
        .click(getDeleteAnalysisButton())
}

/* 
    Renames the saved analysis with the given name to the new name
*/
export async function renameSavedAnalysis(t: TestController, oldAnalysisName: string, newAnalysisName: string): Promise<void> {
    await t
        .click(repeatAnalysisButton)
        .doubleClick(getSavedAnalysisNameDiv(oldAnalysisName))

    // Delete the old analysis name
    await t.pressKey(DELETE_PRESS_KEYS_STRING)

    await t
        .typeText(getActiveElement(), newAnalysisName)
        .pressKey('enter')
}


/*
    If repeating an analysis with imports, this changes the files
    that are imported
*/
export async function repeatAnalysisChangeImports(t: TestController, newImports: {file_names?: string[]}): Promise<void> {
    // Wait a bit, for data to load
    await t.wait(500);

    for (let i = 0; i < newImports.file_names?.length; i++) {
        const fileName = newImports.file_names[i];
        await t
            .click(simpleImportSelect.nth(i))
            .click(simpleImportSelectOption.withExactText(fileName).nth(i))
    }

    await t.click(modalAdvanceButtonSelector)
}
