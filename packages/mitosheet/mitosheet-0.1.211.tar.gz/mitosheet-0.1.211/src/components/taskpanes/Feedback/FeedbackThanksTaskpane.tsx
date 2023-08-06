// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React, { Fragment } from 'react';
import DefaultTaskpane from '../DefaultTaskpane';
import { TaskpaneInfo } from '../taskpanes';
import BlueMitoFolk from '../../icons/mitofolks/BlueMitoFolk';

export type FeedbackThanksTaskpaneProps = {
    setCurrOpenTaskpane: (newTaskpaneInfo: TaskpaneInfo) => void,
};

/* 
    Taskpane that thanks the user for submitting feedback,
    because we really do appreciate it!
*/
function FeedbackThanksTaskpane(props: FeedbackThanksTaskpaneProps): JSX.Element {
    return (
        <DefaultTaskpane
            header = {'Thanks for the Feedback!'}
            setCurrOpenTaskpane={props.setCurrOpenTaskpane}
            taskpaneBody = {
                <Fragment>
                    <p className='txt-16 mb-5px'>
                        If you ever have more feedback, you can find the feedback page through the <b>Docs</b> button in the toolbar above.
                    </p>
                    <BlueMitoFolk bounce loops='3' margin='75px 65px'/>
                </Fragment>
            }
            /* We put a funky-dunky gradient on the taskpane, for fun and profit */
            backgroundImage='linear-gradient(#FFEBEB, #FFE6C8)'
        />
    )

}

export default FeedbackThanksTaskpane;