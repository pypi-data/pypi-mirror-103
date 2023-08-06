import React, { Fragment } from 'react';

/* 
    To create a new tour:
        1. Add the TourName to the TourName enum.
        2. Create a list of steps using the naming: {TourName}TourSteps. aka PivotTourSteps
        3. Add the new Tour to the tours object at the bottom of this file
        4. Add the tour to the displayTour function in Mito.tsx
*/

// Tours is a mapping from tourName to its list of TourSteps
type Tours = {
    [tour in TourName]: TourStep[];
};

/* 
    The name used to identify the tour in the tours mapping. 
    The string declared here is written to the user.json file to register
    that the tour has already been taken.

    Note: changing the strings will cause the user to receive the tour again!
*/
export enum TourName {
    INTRO = 'Intro',
    PIVOT = 'Pivot',
    TUTORIAL = 'Tutorial',
    COLUMN_FORMULAS = 'Column_Formulas',
    EXPLORE_DATA = 'Explore_Datasets',
}

export type TourStep = {
    tourName: TourName,
    stepNumber: number, // we keep track of the step number within each tour for logging
    stepHeader: string,
    stepHeaderBackgroundColor: string,
    stepText?: JSX.Element, // Each tour step must either have a stepText or stepTextFunction
    stepTextFunction?: ((replacementText1: string) => JSX.Element)
    location: TourPopupLocation,
    advanceButtonText: JSX.Element,
    displayBackButton: boolean,
}

// Location to display the TourStep popup
export enum TourPopupLocation {
    BOTTOM_LEFT = 'bottom_left',
    BOTTOM_RIGHT = 'bottom_right',
    TOP_LEFT = 'top_left',
    TOP_RIGHT = 'top_right'
}

const introTourSteps: TourStep[] = [
    {
        tourName: TourName.INTRO,
        stepNumber: 1,
        stepHeader: 'The Mito Spreadsheet',
        stepHeaderBackgroundColor: '#BCDFBC',
        stepText: <div> The Mito Spreadsheet is home base. It&apos;s where you can see your data and write spreadsheet formulas, keeping you connected to your data. </div>,
        location: TourPopupLocation.BOTTOM_LEFT,
        advanceButtonText: <Fragment>Continue &rarr;</Fragment>,
        displayBackButton: false,
    },
    {
        tourName: TourName.INTRO,
        stepNumber: 2,
        stepHeader: 'The Mito Toolbar',
        stepHeaderBackgroundColor: '#DDA1A1',
        stepText: <div> The Mito Toolbar is where you can find Mito’s powerful point and click analysis tools, including pivot tables, merging datasets together, and full screen mode. </div>,
        location: TourPopupLocation.TOP_LEFT,
        advanceButtonText: <Fragment>Continue &rarr;</Fragment>,
        displayBackButton: true
    },
    {
        tourName: TourName.INTRO,
        stepNumber: 3,
        stepHeader: 'The Generated Code',
        stepHeaderBackgroundColor: '#79C2F8',
        stepText: <div>Each time you edit your data, Mito generates the equivalent pandas code in the code cell right below the Mito Sheet. You can run the generated code to keep using the edited dataframes in your notebook as you normally would.</div>,
        location: TourPopupLocation.BOTTOM_LEFT,
        advanceButtonText: <Fragment>Continue &rarr;</Fragment>,
        displayBackButton: true
    },
]

const pivotTourSteps: TourStep[] = [
    {
        tourName: TourName.PIVOT,
        stepNumber: 1,
        stepHeader: 'Creating a Pivot Table',
        stepHeaderBackgroundColor: '#BCDFBC',
        stepText: <div>  <b> Click on the Pivot button</b> to get started. Mito’s pivot tables make it easy to slice and dice your data into different categories. </div>,
        location: TourPopupLocation.BOTTOM_LEFT,
        advanceButtonText: <Fragment>Continue &rarr;</Fragment>,
        displayBackButton: true,
    },
    {
        tourName: TourName.PIVOT,
        stepNumber: 2,
        stepHeader: 'Configure your Pivot Table',
        stepHeaderBackgroundColor: '#DDA1A1',
        stepText: <div> In the open sidebar, <b>select a row and value </b> to create your pivot table.</div>,
        location: TourPopupLocation.BOTTOM_LEFT,
        advanceButtonText: <Fragment>Continue &rarr;</Fragment>,
        displayBackButton: true
    },
    {
        tourName: TourName.PIVOT,
        stepNumber: 3,
        stepHeader: 'That was Easy!',
        stepHeaderBackgroundColor: '#79C2F8',
        stepText: <div>Each time you create a pivot table, a new dataframe is created in the Mito Sheet and the generated code. <b>Checkout the pivot table code below</b>. We just saved our first trip to stack overflow :&#x29; </div>,
        location: TourPopupLocation.BOTTOM_LEFT,
        advanceButtonText: <Fragment>Continue &rarr;</Fragment>,
        displayBackButton: true
    },
]

const ColumnFormulasTourSteps: TourStep[] = [
    {  
        tourName: TourName.COLUMN_FORMULAS,
        stepNumber: 1,
        stepHeader: 'Writing Excel Formulas',
        stepHeaderBackgroundColor: '#BCDFBC',
        stepText: <div>  Mito supports the most popular Excel functions, making it easy to transform your data with the formulas you’re most comfortable with. <b>Click on the Add Col button</b> to create a new column.  </div>,
        location: TourPopupLocation.BOTTOM_LEFT,
        advanceButtonText: <Fragment>Continue &rarr;</Fragment>,
        displayBackButton: true,
    },
    {
        tourName: TourName.COLUMN_FORMULAS,
        stepNumber: 2,
        stepHeader: 'Open the Cell Editor',
        stepHeaderBackgroundColor: '#DDA1A1',
        stepText: <div> <b>Click on any cell in your new column</b> -- it&apos;s to the right of your selected column. <b>Press Enter</b> to open the cell editor. </div>,
        location: TourPopupLocation.BOTTOM_LEFT,
        advanceButtonText: <Fragment>Continue &rarr;</Fragment>,
        displayBackButton: true
    },
    {
        tourName: TourName.COLUMN_FORMULAS,
        stepNumber: 3,
        stepHeader: 'Write your First Formula',
        stepHeaderBackgroundColor: '#79C2F8',
        // eslint-disable-next-line react/display-name
        stepTextFunction: (columnHeader: string): JSX.Element => {
            const text = `In the cell editor, write the formula =LEN(${columnHeader}) and press Enter. The LEN formula returns the length of each cell in column ${columnHeader}.`  
            return (<div>{text}</div>)
        },
        location: TourPopupLocation.BOTTOM_LEFT,
        advanceButtonText: <Fragment>Continue &rarr;</Fragment>,
        displayBackButton: true
    },
    {
        tourName: TourName.COLUMN_FORMULAS,
        stepNumber: 4,
        stepHeader: 'Give your Column a Name',
        stepHeaderBackgroundColor: '#79C2F8',
        // eslint-disable-next-line react/display-name
        stepTextFunction: (columnHeader: string): JSX.Element => {
            const text = `To give your column a more meaningful name, click on its column header. At the top of the sidebar that appears, name the column Len_of_${columnHeader}`  
            return (<div>{text}</div>)
        },
        location: TourPopupLocation.BOTTOM_LEFT,
        advanceButtonText: <Fragment>Continue &rarr;</Fragment>,
        displayBackButton: true
    },
    {
        tourName: TourName.COLUMN_FORMULAS,
        stepNumber: 5,
        stepHeader: "See all of Mito's Formulas",
        stepHeaderBackgroundColor: '#79C2F8',
        stepText: <div>Congrats on writing your first formula! To see a full list of Mito’s functions, <b>click on the Docs</b> button in the top right corner of Mito.</div>,
        location: TourPopupLocation.BOTTOM_LEFT,
        advanceButtonText: <Fragment>Continue &rarr;</Fragment>,
        displayBackButton: true
    },
]

const ExploreDataTourSteps: TourStep[] = [
    {  
        tourName: TourName.EXPLORE_DATA,
        stepNumber: 1,
        stepHeader: 'Exploring Data with Mito',
        stepHeaderBackgroundColor: '#BCDFBC',
        stepText: <div> Mito makes it easy to build intuition for your data by automatically generating summary information about each column. To get started, <b>click on the filter button in the column header</b> of one of your columns.</div>,
        location: TourPopupLocation.BOTTOM_LEFT,
        advanceButtonText: <Fragment>Continue &rarr;</Fragment>,
        displayBackButton: true,
    },
    {
        tourName: TourName.EXPLORE_DATA,
        stepNumber: 2,
        stepHeader: 'View Summary Stats',
        stepHeaderBackgroundColor: '#CAD1FF',
        stepText: <div> <b>Click on the Summary Stats tab </b> at the bottom of the sidebar. The chart at the top shows you the distribution of your column, and there’s more specific summary information down below. Check it out!</div>,
        location: TourPopupLocation.BOTTOM_LEFT,
        advanceButtonText: <Fragment>Continue &rarr;</Fragment>,
        displayBackButton: true
    },
    {
        tourName: TourName.EXPLORE_DATA,
        stepNumber: 3,
        stepHeader: 'Add a Filter',
        stepHeaderBackgroundColor: '#FFDAAE',
        stepText: <div>Now that you have a bit of intuition for your data, <b>switch over to the Filter/Sort Tab </b> to clean up your data. </div>,
        location: TourPopupLocation.BOTTOM_LEFT,
        advanceButtonText: <Fragment>Continue &rarr;</Fragment>,
        displayBackButton: true
    },
    {
        tourName: TourName.EXPLORE_DATA,
        stepNumber: 4,
        stepHeader: "Create a Filter",
        stepHeaderBackgroundColor: '#79C2F8',
        stepText: <div>To add a filter, click on the <b>Add Filter button </b> and then set the filter <b>condition and value</b>. </div>,
        location: TourPopupLocation.BOTTOM_LEFT,
        advanceButtonText: <Fragment>Continue &rarr;</Fragment>,
        displayBackButton: true
    },
    {
        tourName: TourName.EXPLORE_DATA,
        stepNumber: 5,
        stepHeader: "Enjoy your Cleaned Data",
        stepHeaderBackgroundColor: '#FFCBDE',
        stepText: <div>Nice work! In just a few clicks, we’ve built some intuition for our data and removed the values we&apos;re not interested in. </div>,
        location: TourPopupLocation.BOTTOM_LEFT,
        advanceButtonText: <Fragment>Continue &rarr;</Fragment>,
        displayBackButton: true
    },
] 

const tutorialTourSteps: TourStep[] = [
    {
        tourName: TourName.TUTORIAL,
        stepNumber: 1,
        stepHeader: 'Before you Go!',
        stepHeaderBackgroundColor: '#FFDAAE',
        stepText: <div>Clean and analyze your data by writing spreadsheet formulas, visualizing your data, and adding filters. Find a more detailed tutorial <a href="https://docs.trymito.io/getting-started/tutorial" target="_blank" rel="noreferrer" style={{color:'#0081DE'}}>here</a>.</div>,
        location: TourPopupLocation.BOTTOM_LEFT,
        advanceButtonText: <Fragment>Close</Fragment>,
        displayBackButton: true
    }
]

export const tours: Tours = {
    'Intro': introTourSteps,
    'Pivot': pivotTourSteps,
    'Tutorial': tutorialTourSteps,
    'Column_Formulas': ColumnFormulasTourSteps,
    'Explore_Datasets': ExploreDataTourSteps
}

