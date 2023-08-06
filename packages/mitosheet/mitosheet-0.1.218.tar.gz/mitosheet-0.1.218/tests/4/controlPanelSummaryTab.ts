// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

/*
    Contains tests for basic, single sheet mito rendering, column additions,
    and column editing.
*/

import { tryTest } from '../utils/testHelpers';

import { CURRENT_URL } from '../config';

import { 
    columnSummaryGraphSelector, 
    columnSummaryTableSelector, 
    openColumnStatistics 
} from '../utils/columnHelpers';

import { errorMessageSelector } from '../utils/selectors';

fixture `Control Panel Summary Tab`
    .page(CURRENT_URL)

test('Works (no errors) on different column column', async t => {
    await tryTest(
        t,
        `import mitosheet\nimport pandas as pd\ndf = pd.DataFrame({\'A\': [\'A\', \'A\'], \'B\': [123, 2], \'C\': [True, False], \'D\': pd.to_datetime(['12-20-2020', '12-20-2020']), \'E\': ['12-20-2020', True]})\nmitosheet.sheet(df)`, 
        async t => {
            const columns = ['A', 'B', 'C', 'D', 'E'];
            for (let i = 0; i < columns.length; i++) {
                await openColumnStatistics(t, columns[i]);
                await t
                    .expect(errorMessageSelector.exists).notOk()
                    .expect(columnSummaryGraphSelector.exists).ok()
                    .expect(columnSummaryTableSelector.exists).ok()
                    .expect(columnSummaryTableSelector.find('tr').count).gt(0)
            }
            
        }
    )
});