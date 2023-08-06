// Copyright (c) Mito

import React, { Fragment, useState } from 'react';

import '../../../css/large-input.css';

/* 
  A input component created for use in taskpanes
*/
const LargeInput = (props: {
    startingValue: string;
    onSubmit: (value: string) => void;
    placeholderText: string
    extraLarge?: boolean;
}): JSX.Element => {
    const [currentValue, setCurrentValue] = useState<string>(props.startingValue)

    const className = !props.extraLarge ? 'input large-input' : 'input extra-large-input';

    return (
        <Fragment>
            <form onSubmit={async (e) => {e.preventDefault(); await props.onSubmit(currentValue)}}>
                <input 
                    className={className} /* Make sure the input field blends in with the div */
                    type='text'
                    value={currentValue} 
                    onChange={(e) => {setCurrentValue(e.target.value)}}
                    onBlur={() => props.onSubmit(currentValue)}
                    placeholder={props.placeholderText}
                    autoFocus
                />
            </form>
        </Fragment>
    )
}

export default LargeInput
