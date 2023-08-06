// Copyright (c) Mito

import React from 'react';

import { ControlPanelTab } from './ControlPanelTaskpane';

/* 
    The tabs at the bottom of the column control panel that allows users to switch
    from sort/filter to seeing summary statistics about the column
*/
function ControlPanelTaskpaneTabs(
    props: {
        selectedTab: ControlPanelTab, 
        setSelectedColumnControlPanelTab: (tab: ControlPanelTab) => void
    }): JSX.Element {

    return (
        <div className='control-panel-taskpane-tab-container'>
            <div 
                className={'control-panel-taskpane-tab' + (props.selectedTab === ControlPanelTab.FilterSort ? ' selected' : ' unselected')} 
                onClick={() => props.setSelectedColumnControlPanelTab(ControlPanelTab.FilterSort)}
            >
                <p>
                    Filter/Sort
                </p>
            </div>
            <div 
                className={'control-panel-taskpane-tab' + (props.selectedTab === ControlPanelTab.SummaryStats ? ' selected' : ' unselected')} 
                onClick={() => props.setSelectedColumnControlPanelTab(ControlPanelTab.SummaryStats)}
            >
                <p>
                    Summary Stats
                </p>
            </div>
        </div> 
    )
} 

export default ControlPanelTaskpaneTabs;