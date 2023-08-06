// Copyright (c) Mito

import React, { useEffect, useState } from 'react';
import DefaultTaskpane from '../DefaultTaskpane';
import { MitoAPI } from '../../../api';

// Import 
import '../../../../css/import-taskpane.css'
import { TaskpaneInfo } from '../taskpanes';
import LargeSelect from '../../elements/LargeSelect';
import XIcon from '../../icons/XIcon';
import ImportByPathCard from './ImportByPathCard';

interface ImportTaskpaneProps {
    mitoAPI: MitoAPI;
    setCurrOpenTaskpane: (newTaskpaneInfo: TaskpaneInfo) => void,
}

/* 
    The FileImportType is used to tell the UI which import type to display:
    - CURRENT_FOLDER => display select import
    - BY_PATH => input field for paths. 
*/
export enum FileImportType {
    CURRENT_FOLDER = 'current_folder',
    BY_PATH = 'by_path'
}

export interface FileImport {
    path: string;
    importType: FileImportType ;
}

/* 
    Provides a live updating import modal
    that allows users to import data
*/
function ImportTaskpane(props: ImportTaskpaneProps): JSX.Element {

    // Save the step id for overwriting
    const [stepID, setStepID] = useState('');

    // The datafiles are the files loaded from the backend
    const [dataFiles, setDataFiles] = useState<string[]>([]);
    const [hasLoadedDataFiles, setHasLoadedDataFiles] = useState(false);

    // Which files are actually selected by the user
    const [selectedFiles, setSelectedFiles] = useState<FileImport[]>([]);

    /* 
        Sends a message to the backend, importing files (and overwriting
        the step if it already exists).
    */
    async function sendImportMessage(files: FileImport[]) {
        // Collect all of the file paths to submit 
        let filePaths: string[] = files.map(file => file.path)

        // Remove any empty file paths
        filePaths = filePaths.filter(filePath => filePath !== '')
        
        // Send message to backend to process import
        const newStepID = await props.mitoAPI.sendSimpleImportMessage(
            filePaths,
            stepID
        )
        setStepID(newStepID);
    }

    /* 
        Loads the data files from the backend.
    */
    async function getDataFiles() {
        // Loads the data files
        const receivedDataFiles = await props.mitoAPI.getDataFiles();
        setDataFiles(receivedDataFiles);
        // Save that we have loaded the files
        setHasLoadedDataFiles(true);
    }

    // Updates a specific imported file to a specific import
    const updateImportedFile = async (index: number, newImportPath: string, importType: FileImportType): Promise<void> => {
        const newImports = [...selectedFiles];
        newImports[index] = {
            path: newImportPath,
            importType: importType
        }
        setSelectedFiles(newImports);

        // Set a message to actually update this
        await sendImportMessage(newImports);
    }

    // Adds a new file to import by current folder select
    const addNewCurrentFolderFileImport = async (): Promise<void> => {
        const newImports = [...selectedFiles];

        // We take the first file that has not been imported, or if all files have been
        // imported, than just the first file
        let newImport = dataFiles[0];

        const selectedFilePaths = selectedFiles.map(fileObj => fileObj.path)
        const unimportedFiles = dataFiles.filter(fileName => !selectedFilePaths.includes(fileName));
        if (unimportedFiles.length > 0) {
            newImport = unimportedFiles[0];
        }
        
        newImports.push({
            path: newImport,
            importType: FileImportType.CURRENT_FOLDER
        });
        setSelectedFiles(newImports);

        // Send a message to actually update this
        await sendImportMessage(newImports);
    }

    // Adds a new file to import by path.
    // We ue it to create the UI input field
    const addNewByPathFileImport = () => {
        const newImports = [...selectedFiles];
        newImports.push({
            path: '',
            importType: FileImportType.BY_PATH
        })
        setSelectedFiles(newImports);
    }

    const setImportedPath = async (index: number, path: string): Promise<void> => {
        // Update the path of the submitted input field
        const newImports = [...selectedFiles];
        newImports[index].path = path

        // Set the state
        setSelectedFiles(newImports);

        // Send a message to actually update this
        await sendImportMessage(newImports);
    }

    // Removes a file from being imported
    const removeFileImport = async (index: number): Promise<void> => {
        const newImports = [...selectedFiles];

        newImports.splice(index, 1);

        setSelectedFiles(newImports);

        // Send a message to actually update this
        await sendImportMessage(newImports);
    }

    useEffect(() => {
        // We load the data after the component renders
        void getDataFiles();
    }, []) // empty array is necessary to have this run only once

    return (
        <DefaultTaskpane
            header = {'Import CSV Files'}
            setCurrOpenTaskpane={props.setCurrOpenTaskpane}
            taskpaneBody = {
                <React.Fragment>
                    {!hasLoadedDataFiles && 
                        // We display a loading message while loading the files from the backend
                        <div>
                            Loading data files in the current folder...
                        </div>
                    }
                    {hasLoadedDataFiles &&
                        // If we loaded some files, we let users import files
                        <React.Fragment>
                            {selectedFiles.map((fileObj, i) => {
                                if (fileObj.importType === FileImportType.CURRENT_FOLDER) {
                                    return (
                                        <div key={i} className='import-file-select-container'>
                                            <LargeSelect
                                                key={i}
                                                startingValue={fileObj.path}
                                                optionsArray={dataFiles}
                                                setValue={(fileName) => {void updateImportedFile(i, fileName, FileImportType.CURRENT_FOLDER)}}
                                                extraLarge={true}
                                            />
                                            <div className='import-file-delete' onClick={() => {void removeFileImport(i)}}>
                                                <XIcon/>
                                            </div>
                                        </div>
                                    )
                                } else {
                                    return (
                                        // See note below about key. 
                                        <div key={i + fileObj.path} className='import-file-select-container'>
                                            <ImportByPathCard
                                                /* 
                                                    Without setting the key like this, when the user deletes a sheet, 
                                                    it always deletes the last import by path. We're not sure why this
                                                    occurs, but making the keys unique in this way fixes it. 
                                                */
                                                key={i + fileObj.path}  
                                                path={fileObj.path}
                                                setImportedPath={(path) => {void setImportedPath(i, path)}}
                                            />
                                            <div className='import-file-delete' onClick={() => {void removeFileImport(i)}}>
                                                <XIcon/>
                                            </div>
                                        </div>
                                    )
                                }
                            })}
                            {hasLoadedDataFiles && dataFiles.length === 0 &&
                                /* If there are no files in the Current Folder don't let the use click the Add File from Current Folder Button */
                                <div>
                                    <div className='mb-5'>
                                        There are no files in the current folder to import. <br/> <br/>

                                        Upload files to this folder, and then reopen the import taskpane. <br/> <br/>

                                        You can read more about importing <a href='https://docs.trymito.io/getting-started/importing-data-to-mito' target="_blank" rel="noreferrer"><u>here.</u></a>
                                    </div>
                                </div>
                            }
                            {hasLoadedDataFiles && dataFiles.length !== 0 &&
                                <div className='import-add-file-from-current-folder-button' onClick={addNewCurrentFolderFileImport}>
                                    + Add File from Current Folder
                                </div>
                            }
                            <div className='import-add-file-by-path-button' onClick={addNewByPathFileImport}>
                                or <u>Add File by Path</u>
                            </div>
                        </React.Fragment>
                    }
                </React.Fragment>
            }
        />
    )
}

export default ImportTaskpane;