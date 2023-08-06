// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

/*
    Contains tests for basic, single sheet mito rendering, column additions,
    and column editing.
*/

import { tryTest } from '../utils/testHelpers';

import { CURRENT_URL } from '../config';
import { doNewPivot } from '../utils/pivotHelpers';
import { tourCloseButton, tourContinueButton } from '../utils/tourHelpers';
import { Selector } from 'testcafe';

const code = `import pandas as pd

# First, remove the user.json
import os
from pathlib import Path
try:
    os.remove(os.path.join(Path.home(), ".mito", "user.json"))
except:
    pass

import mitosheet
df = pd.DataFrame(data={'A': [1,2,3], 'B': [1,2,3]})
mitosheet.sheet(df)`;

fixture `Test Tour`
    .page(CURRENT_URL)

    
test('Can go through the tour', async t => {
    await tryTest(
        t,
        code, 
        async t => {
            // Click the continue
            await t.click(tourContinueButton)

            // Then click the close button
            await t.click(Selector(tourCloseButton));

            // Click continue on the tutorial popup
            await t.click(tourContinueButton)

            // Make sure the tour closed
            await t.expect(tourContinueButton.exists).notOk()            
        },
        false
    )
});