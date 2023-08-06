// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

/*
    Contains all useful selectors and helpers for interacting with the import modals. 
*/

import { Selector } from 'testcafe';

import { modalAddSelector, modalAdvanceButtonSelector } from './allModals';

// Toolbar Button
export const importButton = Selector('p')
    .withText('Import')
    .parent()

// Which sort of import do you want to do?
export const importMethodSelect = Selector('select.select')
    .nth(0)
export const importMethodSelectOption = importMethodSelect
    .find('option')

export const importAddFromCurrentFolderButton = Selector('div.import-add-file-from-current-folder-button')
export const importAddByPathButton = Selector('div.import-add-file-by-path-button')

// Simple Import Selectors
export const simpleImportSelect = Selector('select.select')
export const simpleImportSelectOption = Selector('select.select')
    .find('option')

// Import By Path Selectors
export const importByPathInput = Selector('input.extra-large-input')

/*
    Does a simple import, importing the passed file_names
*/
export async function doSimpleImportCurrentFolder(t: TestController, file_names: string[]): Promise<void> {
    
    await t
        .click(importButton)
        // We wait here, because data has to be gotten from the API, and sometimes
        // when we move to quick this causes issues. I found it impossible to move
        // this quick in practice. 
        .wait(500)

    // Add space for all of these files
    for (let i = 0; i < file_names.length; i++) {
        await t.click(importAddFromCurrentFolderButton);
    }

    // And then go and actually set the files
    for (let i = 0; i < file_names.length; i++) {
        await t
            .click(simpleImportSelect.nth(i))
            .click(simpleImportSelectOption.withExactText(file_names[i]).nth(i))
    }
}

/*
    Does a simple import, importing the passed file_names
*/
export async function doSimpleImportByPath(t: TestController, file_paths: string[]): Promise<void> {
    
    await t
        .click(importButton)
        // We wait here, because data has to be gotten from the API, and sometimes
        // when we move to quick this causes issues. I found it impossible to move
        // this quick in practice. 
        .wait(500)

    // Add space for all of these files
    for (let i = 0; i < file_paths.length; i++) {
        await t.click(importAddByPathButton);
    }

    // And then go and actually set the files
    for (let i = 0; i < file_paths.length; i++) {
        await t
            .click(importByPathInput.nth(i))
            .typeText(importByPathInput.nth(i), file_paths[i])
    }
}