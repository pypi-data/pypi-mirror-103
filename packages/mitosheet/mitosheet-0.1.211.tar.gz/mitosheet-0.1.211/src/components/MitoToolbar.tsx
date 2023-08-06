// Copyright (c) Mito

import React, { useState } from 'react';
import fscreen from 'fscreen';

// Import CSS
import "../../css/mito-toolbar.css"


// Import Types
import { SheetJSON } from '../widget';
import { ModalInfo, ModalEnum } from './Mito';

// Import Components 
import { TaskpaneInfo, TaskpaneType } from './taskpanes/taskpanes';
import { MitoAPI } from '../api';

// Icons!
import UndoIcon from './icons/UndoIcon';
import ImportIcon from './icons/ImportIcon';
import ExportIcon from './icons/ExportIcon';
import ReplayIcon from './icons/ReplayIcon';
import SaveIcon from './icons/SaveIcon';
import MergeIcon from './icons/MergeIcon';
import PivotIcon from './icons/PivotIcon';
import DeleteColumnIcon from './icons/DeleteColumnIcon';
import AddColumnIcon from './icons/AddColumnIcon';
import DocumentationIcon from './icons/DocumentationIcon';
import { CloseFullscreenIcon, OpenFullscreenIcon } from './icons/FullscreenIcons';
import StepsIcon from './icons/StepsIcon';
import FastForwardIcon from './icons/FastForwardIcon';

const MitoToolbar = (
    props: {
        mitoContainerRef: HTMLDivElement | undefined | null,
        sheetJSON: SheetJSON, 
        selectedSheetIndex: number,
        setEditingMode: (on: boolean, column: string, rowIndex: number) => void,
        setModal: (modal: ModalInfo) => void,
        model_id: string,
        selectedColumn: string,
        setCurrOpenTaskpane: (newCurrTaskpane: TaskpaneInfo) => void;
        mitoAPI: MitoAPI
        closeOpenEditingPopups: () => void;
        currStepIdx: number;
        numSteps: number;
        highlightPivotTableButton: boolean;
        highlightAddColButton: boolean;

    }): JSX.Element => {

    /* Adds a new column onto the end of a sheet, with A, B, C... as the name */
    const addColumn = () => {
        // We turn off editing mode, if it is on
        props.setEditingMode(false, "", -1);

        // we close the editing taskpane if its open
        props.closeOpenEditingPopups();

        /*
        * Helper function that, given a number, returns Excel column that corresponds to this number (1-indexed)
        */
        function toColumnName(num: number): string {
            let ret;
            let a = 1;
            let b = 26;
            for (ret = ''; (num -= a) >= 0; a = b, b *= 26) {
                ret = String.fromCharCode(Math.round((num % b) / a) + 65) + ret;
            }
            return ret;
        }

        let inc = 1;
        let newColumnHeader = toColumnName(props.sheetJSON.columns.length + inc);
        // If the column header is in the sheet already, we bump and keep trying
        while (props.sheetJSON.columns.includes(newColumnHeader)) {
            inc++;
            newColumnHeader = toColumnName(props.sheetJSON.columns.length + inc);
        }

        // The new column should be placed 1 position to the right of the selected column
        const newColumnHeaderIndex = props.sheetJSON.columns.findIndex((columnHeader) => columnHeader === props.selectedColumn) + 1

        void props.mitoAPI.sendColumnAddMessage(
            props.selectedSheetIndex,
            newColumnHeader,
            newColumnHeaderIndex
        );
    }


    /* Undoes the last step that was created */
    const undo = () => {
        // We turn off editing mode, if it is on
        props.setEditingMode(false, "", -1);

        // we close the editing taskpane if its open
        props.closeOpenEditingPopups();

        void props.mitoAPI.sendUndoMessage();
    }

    /* Saves the current file as as an exported analysis */
    const downloadAnalysis = () => {
        // We turn off editing mode, if it is on
        props.setEditingMode(false, "", -1);

        // we close the editing taskpane if its open
        props.closeOpenEditingPopups();
        
        props.setModal({type: ModalEnum.Download});
    }

    
    const [fullscreen, setFullscreen] = useState(false);
    fscreen.onfullscreenchange = () => {
        setFullscreen(!!fscreen.fullscreenElement)
        
        void props.mitoAPI.sendLogMessage(
            'button_toggle_fullscreen',
            {
                // Note that this is true when _end_ in fullscreen mode, and 
                // false when we _end_ not in fullscreen mode, which is much
                // more natural than the alternative
                fullscreen: !!fscreen.fullscreenElement
            }
        )
    };
    
    /* 
        Toggles if Mito is full screen or not
    */
    const toggleFullscreen = () => {
        // We toggle to the opposite of whatever the fullscreen actually is (as detected by the
        // fscreen library), and then we set the fullscreen state variable to that state (in the callback
        // above), so that the component rerenders propery
        const isNotFullscreen = fscreen.fullscreenElement === undefined || fscreen.fullscreenElement === null;
        if (isNotFullscreen && props.mitoContainerRef) {
            fscreen.requestFullscreen(props.mitoContainerRef);
        } else {
            fscreen.exitFullscreen();
        }
    }

    const openDocumentation = () => {
        // We turn off editing mode, if it is on
        props.setEditingMode(false, "", -1);

        // We log the opening of the documentation taskpane
        void props.mitoAPI.sendLogMessage(
            'button_documentation_log_event',
            {
                stage: 'opened'
            }
        );

        // we open the documentation taskpane
        props.setCurrOpenTaskpane({type: TaskpaneType.DOCUMENTATION});
    }

    const openMerge = () => {
        // We turn off editing mode, if it is on
        props.setEditingMode(false, "", -1);

        // We open the merge taskpane
        props.setCurrOpenTaskpane({type: TaskpaneType.MERGE});
    }

    const openPivotTable = () => {
        // We turn off editing mode, if it is on
        props.setEditingMode(false, "", -1);

        props.setCurrOpenTaskpane({type: TaskpaneType.PIVOT});
    }

    const openDeleteColumn = () => {
        // We turn off editing mode, if it is on
        props.setEditingMode(false, "", -1);

        // we close the editing taskpane if its open
        props.closeOpenEditingPopups();

        // TODO: log here, and in all the rest of these functions

        props.setModal({type: ModalEnum.DeleteColumn, columnHeader: props.selectedColumn});
    }

    const openSave = () => {
        // We turn off editing mode, if it is on
        props.setEditingMode(false, "", -1);

        // we close the editing taskpane if its open
        props.closeOpenEditingPopups();

        props.setModal({type: ModalEnum.SaveAnalysis});
    }

    
    const openReplay = () => {
        // We turn off editing mode, if it is on
        props.setEditingMode(false, "", -1);

        // we close the editing taskpane if its open
        props.closeOpenEditingPopups();
        
        props.setCurrOpenTaskpane({type: TaskpaneType.REPLAY_ANALYSIS});
    }
    
    const openImport = () => {
        // We turn off editing mode, if it is on
        props.setEditingMode(false, "", -1);

        // we close the editing taskpane if its open
        props.closeOpenEditingPopups();

        props.setCurrOpenTaskpane({type: TaskpaneType.IMPORT});
    }

    const openSteps = () => {
        void props.mitoAPI.sendLogMessage('click_open_steps')
        props.setCurrOpenTaskpane({type: TaskpaneType.STEPS});
    }


    const fastForward = () => {
        // Fast forwards to the most recent step, allowing editing
        void props.mitoAPI.sendLogMessage('click_fast_forward')
        void props.mitoAPI.checkoutStepByIndex(props.numSteps - 1);
    }

    // Class used to highlight the pivot table toolbar item used by Tour.tsx
    const highlightPivotTableButtonClass = props.highlightPivotTableButton ? 'mito-toolbar-item-draw-attention' : '';
    const highlightAddColButtonClass = props.highlightAddColButton ? 'mito-toolbar-item-draw-attention' : '';


    return (
        <div className='mito-toolbar-container'>
            <div className='mito-toolbar-container-left'>
                <button className='mito-toolbar-item vertical-align-content' onClick={undo}>
                    <div className='mito-toolbar-item-icon-container'>
                        <UndoIcon/>
                    </div>
                    <p className='mito-toolbar-item-label'> 
                        Undo
                    </p>
                </button>

                <div className="vertical-line mt-1"/>

                <button className='mito-toolbar-item vertical-align-content' id='tour-import-button-id' onClick={openImport}>
                    <div className='mito-toolbar-item-icon-container'>
                        <ImportIcon/>
                    </div>
                    <p className='mito-toolbar-item-label'> 
                        Import
                    </p>
                </button>

                <button className='mito-toolbar-item vertical-align-content' onClick={downloadAnalysis}>
                    <div className='mito-toolbar-item-icon-container'>
                        <ExportIcon/>
                    </div>
                    <p className='mito-toolbar-item-label'> 
                        Export
                    </p>
                </button>

                <div className="vertical-line mt-1"/>

                <button className={'mito-toolbar-item vertical-align-content ' + highlightAddColButtonClass} onClick={addColumn}>
                    <div className='mito-toolbar-item-icon-container'>
                        <AddColumnIcon/>
                    </div>
                    <p className='mito-toolbar-item-label'> 
                        Add Col
                    </p>
                </button>
                <button className='mito-toolbar-item vertical-align-content' onClick={openDeleteColumn}>
                    <div className='mito-toolbar-item-icon-container'>
                        <DeleteColumnIcon/>
                    </div>
                    <p className='mito-toolbar-item-label'> 
                        Del Col
                    </p>
                </button>
                <div className="vertical-line mt-1"></div>
                <button className={'mito-toolbar-item ' + highlightPivotTableButtonClass} onClick={openPivotTable}>
                    <div className='mito-toolbar-item-icon-container'>
                        <PivotIcon/>
                    </div>
                    <p className='mito-toolbar-item-label'> 
                        Pivot
                    </p>
                </button>
                <button className='mito-toolbar-item' onClick={openMerge}>
                    <div className='mito-toolbar-item-icon-container'>
                        <MergeIcon/>
                    </div>
                    <p className='mito-toolbar-item-label'> 
                        Merge
                    </p>
                </button>
                <div className="vertical-line mt-1"></div>
                <button className='mito-toolbar-item' onClick={openSave}>
                    <div className='mito-toolbar-item-icon-container'>
                        <SaveIcon/>
                    </div>
                    <p className='mito-toolbar-item-label'> 
                        Save
                    </p>
                </button>
                <button className='mito-toolbar-item' onClick={openReplay}>
                    <div className='mito-toolbar-item-icon-container'>
                        <ReplayIcon/>
                    </div>
                    <p className='mito-toolbar-item-label'> 
                        Replay
                    </p>
                </button>
            </div>
            <div className='mito-toolbar-container-right mr-1'>
                {/* 
                    Only when we are not caught up do we display the fast forward button
                */}
                {props.currStepIdx !== props.numSteps - 1 &&
                    <button className='mito-toolbar-item' onClick={fastForward}>
                        <div className='mito-toolbar-item-icon-container'>
                            <FastForwardIcon/>
                        </div>
                        <p className='mito-toolbar-item-label'> 
                            Fast Forward
                        </p>
                    </button>
                }
                
                <button className='mito-toolbar-item' onClick={openSteps}>
                    <div className='mito-toolbar-item-icon-container'>
                        <StepsIcon/>
                    </div>
                    <p className='mito-toolbar-item-label'> 
                        Steps
                    </p>
                </button>
                <button className='mito-toolbar-item' onClick={openDocumentation}>
                    <div className='mito-toolbar-item-icon-container'>
                        <DocumentationIcon/>
                    </div>
                    <p className='mito-toolbar-item-label'> 
                        Docs
                    </p>
                </button>
                {/* We show a different icon depending if it is fullscreen or not*/}
                {fullscreen &&
                    /* 
                        We put the button inside the conditional render to maintain the structure of 
                        of the html so fix spacing issues on chrome.
                    */
                    <button className='mito-toolbar-item' onClick={toggleFullscreen}>
                        <div className='mito-toolbar-item-icon-container'>
                            <CloseFullscreenIcon/>
                        </div>
                        <p className='mito-toolbar-item-label'> 
                            Fullscreen
                        </p>
                    </button>
                }
                {!fullscreen &&
                    <button className='mito-toolbar-item' onClick={toggleFullscreen}>
                        <div className='mito-toolbar-item-icon-container'>
                            <OpenFullscreenIcon/>
                        </div>
                        <p className='mito-toolbar-item-label'> 
                            Fullscreen
                        </p>
                    </button>
                }
            </div>
        </div>
    );
};

export default MitoToolbar;