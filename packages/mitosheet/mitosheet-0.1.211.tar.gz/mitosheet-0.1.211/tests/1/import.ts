// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

/*
    Contains tests for importing data.
*/

import { tryTest, clearAllCreateNewNotebook } from '../utils/testHelpers';

import {
    checkSheets,
} from '../utils/helpers';

import {
    doSimpleImportByPath,
    doSimpleImportCurrentFolder
} from '../utils/importHelpers';
import { repeatAnalysis, repeatAnalysisChangeImports } from '../utils/repeatAnalysisHelpers';
import { saveAnalysis } from '../utils/saveAnalysisHelpers';
import { checkGeneratedCode } from '../utils/generatedCodeHelpers';


const code = `
import pandas as pd
import mitosheet

df1 = pd.DataFrame(data={'A': [1, 2, 3], 'B': [4, 5, 6]})
df1.to_csv("df1.csv", index=False)

df2 = pd.DataFrame(data={'A': [7, 8, 9], 'B': [10, 11, 12]})
df2.to_csv("df2.csv", index=False)

mitosheet.sheet()
`
import { CURRENT_URL } from '../config';

fixture `Test Import`
    .page(CURRENT_URL)

test('Can do a simple import', async t => {
    await tryTest(
        t,
        code,
        async t => {
            await doSimpleImportCurrentFolder(t, ['df1.csv', 'df2.csv'])
            await checkSheets(t, {
                'df1_csv': {
                    'A': ['1', '2', '3'],
                    'B': ['4', '5', '6']
                },
                'df2_csv': {
                    'A': ['7', '8', '9'],
                    'B': ['10', '11', '12']
                }
            })
        }
    )
});

test('Can save a simple import, prompted to change dataframes', async t => {
    await tryTest(
        t,
        code,
        async t => {
            await doSimpleImportCurrentFolder(t, ['df1.csv', 'df2.csv'])
            const analysisName = await saveAnalysis(t);

            // Reset the notebook
            await clearAllCreateNewNotebook(t, code);

            await repeatAnalysis(t, analysisName);
            await repeatAnalysisChangeImports(t, {file_names: ['df1.csv', 'df1.csv']});
            await checkSheets(t, {
                'df1_csv': {
                    'A': ['1', '2', '3'],
                    'B': ['4', '5', '6']
                },
                'df1_csv_0': {
                    'A': ['1', '2', '3'],
                    'B': ['4', '5', '6']
                }
            })
        }
    )
});


const fileNameCode = `
import pandas as pd
import mitosheet

df1 = pd.DataFrame(data={'A': [1, 2, 3], 'B': [4, 5, 6]})
df1.to_csv("df1.csv", index=False)

# Pass in a string and a dataframe
mitosheet.sheet('df1.csv', df1)
`

test('Can pass a filename, generates valid code', async t => {
    await tryTest(
        t,
        fileNameCode,
        async t => {

            await checkSheets(t, {
                'df1_csv': {
                    'A': ['1', '2', '3'],
                    'B': ['4', '5', '6']
                },
                'df1': {
                    'A': ['1', '2', '3'],
                    'B': ['4', '5', '6']
                },
            })

            await checkGeneratedCode(t, 'df1_csv', {
                'A': ['1', '2', '3'],
                'B': ['4', '5', '6']
            })
        }
    )
});

const createFilesToImportAndRenderMito = `
import pandas as pd
import mitosheet

df1 = pd.DataFrame(data={'A': [1, 2, 3], 'B': [4, 5, 6]})
df1.to_csv("../df1.csv", index=False)

df2 = pd.DataFrame(data={'A': [1, 2, 3], 'B': [4, 5, 6]})
df2.to_csv("../df2.csv", index=False)

df3 = pd.DataFrame(data={'A': [1, 2, 3], 'B': [4, 5, 6]})
df3.to_csv("df2.csv", index=False) # We add this file to get to the correct import taskpane screen

# Pass in a string and a dataframe
mitosheet.sheet()
`

test('Can use import taskpane for path inputs', async t => {
    await tryTest(
        t,
        createFilesToImportAndRenderMito,
        async t => {

            await doSimpleImportByPath(t, ['../df1.csv', '../df2.csv'])

            await checkGeneratedCode(t, 'df1_csv', {
                'A': ['1', '2', '3'],
                'B': ['4', '5', '6']
            })
        }
    )
});