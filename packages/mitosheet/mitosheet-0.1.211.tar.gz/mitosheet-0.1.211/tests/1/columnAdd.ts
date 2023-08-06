// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

/*
    Contains tests for basic, single sheet mito rendering, column additions,
    and column editing.
*/

import { tryTest } from '../utils/testHelpers';

import {
    addColumnButton
} from '../utils/columnHelpers'

import { 
    checkSheet,
    DELETE_PRESS_KEYS_STRING,
} from '../utils/helpers';


import { CURRENT_URL } from '../config';
import { checkGeneratedCode } from '../utils/generatedCodeHelpers';
import { getCellSelector } from '../utils/selectors';
import { Selector } from 'testcafe';

fixture `Column Additions`
    .page(CURRENT_URL)

test('Can add two columns then set formula by using mouse', async t => {
    await tryTest(
        t,
        'import pandas as pd\nimport mitosheet\ndf = pd.DataFrame(data={\'A\': [1, 2, 3]})\nmitosheet.sheet(df)',
        async t => {
            await t.click(addColumnButton);
            await t.click(addColumnButton);

            const cell = getCellSelector('C', '1');

            await t
                .click(cell)
                .pressKey('enter')
                .selectText(Selector('input.ag-cell-inline-editing'))
                // NOTE: somehow, this deletes whatever formula is there, no matter how
                // long the formula is... I'll take it!
                .pressKey(DELETE_PRESS_KEYS_STRING)
                .click(getCellSelector('A', '1'))
                .pressKey('enter')


            await checkSheet(t, {
                'A': ['1', '2', '3'],
                'C': ['1', '2', '3'],
                'B': ['0', '0', '0']
            });

            const expectedDf = {
                'A': ['1', '2', '3'],
                'C': ['1', '2', '3'],
                'B': ['0', '0', '0']
            }

            await checkGeneratedCode(t, 'df', expectedDf)
        }
    )
});