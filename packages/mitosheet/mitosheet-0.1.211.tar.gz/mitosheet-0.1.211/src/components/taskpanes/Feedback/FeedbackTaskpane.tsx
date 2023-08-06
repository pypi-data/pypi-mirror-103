// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React, { Fragment, useEffect, useState } from 'react';
import DefaultTaskpane from '../DefaultTaskpane';
import { MitoAPI } from '../../../api';

import '../../../../css/feedback-taskpane.css'

// Import 
import { TaskpaneInfo, TaskpaneType } from '../taskpanes';
import NPS, { NetPromotorScore } from './NPS';
import FrustrationSelection, { FrustrationRating } from './FrustrationSelection';

// Keeps track of where you access feedback from
// so we know what is effective for getting feedback
// from users
export enum FeedbackOpenLocation {
    AUTO_POPUP = 'Automatically Popped Up',
    FROM_DOCUMENTATION = 'From Documentation'
}


export type FeedbackTaskpaneProps = {
    setCurrOpenTaskpane: (newTaskpaneInfo: TaskpaneInfo) => void,
    mitoAPI: MitoAPI,
    openLocation: FeedbackOpenLocation
};

/* 
    Taskpane that allows a user to submit feedback on their 
    usage of Mito so far
*/
function FeedbackTaskpane(props: FeedbackTaskpaneProps): JSX.Element {
    const NPSQuestion = 'How likely are you to reccomend Mito to a colleague or friend?';
    const [selectedNPS, setSelectedNPS] = useState<NetPromotorScore>(undefined);

    const ImprovementsQuestion = 'What can we add or change to improve your experience with Mito?';
    const [improvementText, setImprovementText] = useState('');

    const FrustrationQuestion = 'It was frustrating to find the functionality I wanted to use.';
    const [selectedFrustrationRating, setSelectedFrustrationRating] = useState<FrustrationRating | undefined>(undefined);

    // Wrap the setter for selectedNPS so that we can log changes easily
    const changeSelectedNPS = (newSelectedNPS: NetPromotorScore) => {
        // We log that the user switched
        void props.mitoAPI.sendLogMessage('changed_nps_score', {
            'old_selected_nps': selectedNPS,
            'new_selected_nps': newSelectedNPS,
        })

        // Then we actually set the value
        setSelectedNPS(newSelectedNPS);
    }
    
    const submitFeedback = () => {
        // Send a message to the backend with this feedback
        void props.mitoAPI.sendFeedback({
            'opened_location': props.openLocation,
            [NPSQuestion]: selectedNPS,
            [ImprovementsQuestion]: improvementText,
            [FrustrationQuestion]: selectedFrustrationRating
        })
        // Then, advance to the feedback thanks taskpane, to thank them
        // because we really seriously do appreciate the feedback!
        props.setCurrOpenTaskpane({type: TaskpaneType.FEEDBACK_THANKS});
    }

    useEffect(() => {
        // We log where we opened it from, making sure to only run this once
        void props.mitoAPI.sendLogMessage('opened_feedback', {'open_location': props.openLocation})
    }, []);

    return (
        <DefaultTaskpane
            header = {'How is Mito so far?'}
            setCurrOpenTaskpane={props.setCurrOpenTaskpane}
            taskpaneBody = {
                <Fragment>
                    <p className='mb-5px txt-15'>
                        {NPSQuestion}
                    </p>
                    <NPS
                        selectedNPS={selectedNPS}
                        setSelectedNPS={changeSelectedNPS}
                    />
                    <p className='mb-5px mt-15px txt-15'>
                        {ImprovementsQuestion}
                    </p>
                    <textarea
                        className='feedback-taskpane-textarea'
                        value={improvementText}
                        onChange={(event: React.ChangeEvent<HTMLTextAreaElement>) => {setImprovementText(event.target.value)}}
                    />
                    <p className='mb-5px mt-15px txt-15'>
                        {FrustrationQuestion}
                    </p>
                    <FrustrationSelection
                        selectedFrustrationRating={selectedFrustrationRating}
                        setSelectedFrustrationRating={setSelectedFrustrationRating}
                        justifyContent='space-between'
                    />
                    <button className='blue-button txt-16' onClick={submitFeedback}>Send Feedback</button> 
                </Fragment>
            }
            callbackOnClose={() => {
                // If the feedback is closed, we set that the user closed the feedback,
                void props.mitoAPI.setClosedFeedback();

                // And we also log that they closed the feedback, including where they got it from
                void props.mitoAPI.sendLogMessage('closed_feedback', {'open_location': props.openLocation});
            }}
        />
    )

}

export default FeedbackTaskpane;