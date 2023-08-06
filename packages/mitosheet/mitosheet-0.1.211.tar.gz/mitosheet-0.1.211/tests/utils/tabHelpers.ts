

import { Selector } from 'testcafe';
import { DELETE_PRESS_KEYS_STRING } from './helpers';
import { getActiveElement } from './selectors';

/* 
    Helper function that returns a selector for a tab with the passed
    tab name. 

    NOTE: don't use this to click on the tab (see getTabNameSelector)
    as this may accidently click the sheet tab actions.
*/
const getWholeTabSelector = (tabName: string): Selector => {    
    return Selector('p.tab-sheet-name')
        .withExactText(tabName)
        .parent()
        .parent()
}


export const getSelectedTab = (): Selector => {
    return Selector('div.selected-tab')
}

/* 
    Helper function that returns a selector for a tab name only part of
    the tab name, to make sure we don't select the sheet tab actions
    when clicking it
*/
export const getTabNameSelector = (tabName: string): Selector => {    
    return Selector('p.tab-sheet-name')
        .withExactText(tabName)
}

/* 
    Opens the tab actions
*/
export const getTabActionSelector = (tabName: string): Selector => {   
    return getWholeTabSelector(tabName).find('svg');
}

const deleteSelector = Selector('div.sheet-tab-action').withExactText('Delete');
const duplicateSelector = Selector('div.sheet-tab-action').withExactText('Duplicate');
const renameSelector = Selector('div.sheet-tab-action').withExactText('Rename');

export async function deleteSheet(t: TestController, dfName: string): Promise<void> {
    await t
        .click(getTabActionSelector(dfName))
        .click(deleteSelector)
}

export async function duplicateSheet(t: TestController, dfName: string): Promise<void> {
    await t
        .click(getTabActionSelector(dfName))
        .click(duplicateSelector)
}

export async function renameSheet(t: TestController, oldDfName: string, newDfName: string): Promise<void> {
    await t
        .click(getTabActionSelector(oldDfName))
        .click(renameSelector)
        .pressKey(DELETE_PRESS_KEYS_STRING)
        .typeText(getActiveElement(), newDfName)
        .pressKey('enter')
}
