// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React from 'react';

import '../../../../css/nps.css'

export type NetPromotorScore = undefined | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10;

export type NPSProps = {
    selectedNPS: NetPromotorScore;
    setSelectedNPS: (newNetPromotorScore: NetPromotorScore) => void;
};

/* 
    Displays the net promotor score buttons that a user can click
*/
function NPS(props: NPSProps): JSX.Element {

    return (
        <div className='nps-container'>
            {[...Array(11).keys()].map((nps) => {
                const selected = nps === props.selectedNPS;
                const backgroundColor = selected ? 'var(--mito-blue)' : 'white';

                return (
                    <div 
                        className='nps-option'
                        style={{backgroundColor: backgroundColor}} 
                        key={nps} 
                        onClick={() => {
                            // We let you toggle the selection on and off
                            if (selected) {
                                props.setSelectedNPS(undefined)
                            } else {
                                props.setSelectedNPS(nps as NetPromotorScore)
                            }      
                        }}
                    >
                        <p className='m-auto'>
                            {nps}
                        </p>
                    </div>
                )
            })}
        </div>
    )

}

export default NPS;