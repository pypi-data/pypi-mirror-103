// Copyright (c) Mito

import React from 'react';
import LargeInput from '../../elements/LargeInput';

/* 
  The ImportByPathCard is displays instructions to fill in the path when the path is currently ''. 
  Otherwise, it just displays an input field that is stylized similarly to the LargeSelect to make
  the import taskpane look uniform. 
*/
const ImportByPathCard = (props: {
    path: string,
    setImportedPath: (value: string) => void
}): JSX.Element => {

    // If the placeholder text is '', then display the border + instructions telling the user to set a path 
    const className = props.path === '' ? 'import-by-path-card import-by-path-card-border' : 'import-by-path-card'

    // Get placeholder text for the input field depending on if the user is on Mac or not. 
    const placeholderText = window.navigator.userAgent.indexOf("Mac") != -1 ? "/Users/Julia/Documents/airplane.csv" : "C:\\Documents\\data\\airplane.csv"

    return (
        <div className={className}>
            {props.path === '' && 
                <p className='import-by-path-card-title'>Enter the path of the file to import</p>
            }
            <LargeInput
                /* 
                    We add the path here to make sure that the correct input fields get re-rendered. 
                    This corrects a bug where deleting a LargeInput field would re-render the wrong ones, 
                    making the UI out of date with the state. 

                    Note: I'm not sure why this occurs for the inputs, but not the selects in the ImportTaskpane.
                */ 
                startingValue={props.path}
                onSubmit={props.setImportedPath}
                placeholderText={placeholderText}
                extraLarge={true}
            />
        </div>   
    )
} 

export default ImportByPathCard