// Copyright (c) Mito

import React from 'react';

// import css
import "../../../css/default-taskpane.css"
import XIcon from '../icons/XIcon';
import { TaskpaneInfo, TaskpaneType } from './taskpanes';

/*
    DefaultTaskpane is a higher-order component that
    takes a header and a taskpaneBbody, and displays it as a component.

    The modal has props
    - a header string to be shown at the top of the taskpane
    - a taskpaneBody, a react fragment which is the center segment of the taskpane
    - a setTaskpaneOpenOrClosed function to close the taskpane
*/
const DefaultTaskpane = (
    props: {
        header: string
        taskpaneBody: React.ReactFragment
        setCurrOpenTaskpane: (newTaskpaneInfo: TaskpaneInfo) => void;
        /* 
            If you want to put a gradient on the taskpane, you can
            add a background image with a gradient
        */
        backgroundImage?: string;
        /* 
            If you want to run a function when the taskpane
            closes (e.g. for specific logging reasons), use this
        */
        callbackOnClose?: () => void;
        
        
    }): JSX.Element => {

    return (
        <div className='default-taskpane-div' style={{backgroundImage: props.backgroundImage}}>
            <div className='default-taskpane-header-div'>
                <p className='default-taskpane-header-text'>
                    {props.header}
                </p>        
                <div 
                    className='default-taskpane-header-exit-button-div' 
                    onClick={() => {
                        // Call the on close callback, if it exists
                        if (props.callbackOnClose) {
                            props.callbackOnClose();
                        }
                        props.setCurrOpenTaskpane({type: TaskpaneType.NONE});
                    }    
                    }
                >
                    <XIcon/>
                </div>
            </div>
            <div className='default-taskpane-body-div'> 
                {props.taskpaneBody}
            </div>
        </div>
    )
};

export default DefaultTaskpane;