// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React from 'react';

import '../../../../css/frustration-selection.css'

export enum FrustrationRating {
    Frustrating = "It was frustrating.",
    Ok = "It was ok.",
    Easy = "It was easy.",
}

const FRUSTRATION_COLORS = {
    [FrustrationRating.Frustrating]: '#FF6666',
    [FrustrationRating.Ok]: '#FFC989',
    [FrustrationRating.Easy]: '#96D394',

}


/* 
    An internal component that is just responsible for 
    being an actual box that says a specific frustration
*/
function FrustrationSelectionBox(
    props: {
        frustrationRating: FrustrationRating;
        selectedFrustrationRating: FrustrationRating | undefined;
        setSelectedFrustrationRating: (newSelectedFrustrationRating: FrustrationRating | undefined) => void;
        padding?: string
    }): JSX.Element {
    return (
        <div 
            className='frustration-selection-box'
            style={{
                padding: props.padding || '',
                backgroundColor: FRUSTRATION_COLORS[props.frustrationRating], 
                border: props.selectedFrustrationRating === props.frustrationRating ? '2px solid black' : '2px solid white'}
            } 
            onClick={() => {
                // We let you toggle the selection on and off
                if (props.selectedFrustrationRating === props.frustrationRating) {
                    props.setSelectedFrustrationRating(undefined)
                } else {
                    props.setSelectedFrustrationRating(props.frustrationRating)
                }      
            }}
        >
            <p className='m-auto'>
                {props.frustrationRating}
            </p>
        </div>
    )
}


export type FrustrationSelectionProps = {
    selectedFrustrationRating: FrustrationRating | undefined;
    setSelectedFrustrationRating: (newSelectedFrustrationRating: FrustrationRating | undefined) => void;
    justifyContent?: string;
    padding?: string
};

/* 
    Displays three boxes that the user can click
    rating an experience between frustrating and
    easy.
*/
function FrustrationSelection(props: FrustrationSelectionProps): JSX.Element {
    return (
        <div className='frustration-selection-wrapper' style={{
            justifyContent: props.justifyContent || '',
        }}>
            <FrustrationSelectionBox
                frustrationRating={FrustrationRating.Frustrating}
                selectedFrustrationRating={props.selectedFrustrationRating}
                setSelectedFrustrationRating={props.setSelectedFrustrationRating}
                padding={props.padding}
            />
            <FrustrationSelectionBox
                frustrationRating={FrustrationRating.Ok}
                selectedFrustrationRating={props.selectedFrustrationRating}
                setSelectedFrustrationRating={props.setSelectedFrustrationRating}
                padding={props.padding}
            />
            <FrustrationSelectionBox
                frustrationRating={FrustrationRating.Easy}
                selectedFrustrationRating={props.selectedFrustrationRating}
                setSelectedFrustrationRating={props.setSelectedFrustrationRating}
                padding={props.padding}
            />
        </div>
    )
}

export default FrustrationSelection;