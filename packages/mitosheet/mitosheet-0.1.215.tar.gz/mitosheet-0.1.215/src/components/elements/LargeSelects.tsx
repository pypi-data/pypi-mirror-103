// Copyright (c) Mito

import React, { Fragment } from 'react';

import LargeSelect from './LargeSelect';
import '../../../css/large-select.css';

/* 
  An element that allows you to create mulitple large selects, all with the same options
  and the same starting value.
*/
const LargeSelects = (props: {
    numSelects: number,
    startingValue: undefined | string | string[],
    optionsArray: string[],
    setValue: (index: number, value: string) => void,
    extraLarge?: boolean;
}): JSX.Element => {

    const largeSelects = [];
    for (let i = 0; i < props.numSelects; i++) {
        let startingValue: string | undefined = undefined;
        if (Array.isArray(props.startingValue)) {
            startingValue = props.startingValue[i];
        } else {
            startingValue = props.startingValue;
        }

        largeSelects.push((
            <LargeSelect
                key={i}
                startingValue={startingValue}
                optionsArray={props.optionsArray}
                setValue={(value) => {props.setValue(i, value)}}
                extraLarge={props.extraLarge}
            />
        ))
    }

    return (
        <Fragment>
            {largeSelects}
        </Fragment>
    )
}

export default LargeSelects
