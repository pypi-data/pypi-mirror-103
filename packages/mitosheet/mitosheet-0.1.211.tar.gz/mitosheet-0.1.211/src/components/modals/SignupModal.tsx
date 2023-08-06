// Copyright (c) Mito

import React, { FormEvent, useState, useRef, useEffect } from 'react';
import { ModalEnum, ModalInfo } from '../Mito';
import { MitoAPI } from '../../api';
import BlueMitoFolk from '../icons/mitofolks/BlueMitoFolk';
import PinkMitoFolk from '../icons/mitofolks/PinkMitoFolk';
import YellowMitoFolk from '../icons/mitofolks/YellowMitoFolk';
import FrustrationSelection, { FrustrationRating } from '../taskpanes/Feedback/FrustrationSelection';

import '../../../css/signup-modal.css';

/* 
    This file contains all the screens used in the signup modal. As these
    are only used in this one file, we keep them together for cleanlyness.
*/


/* Step one requires an email input */
const StepOne = (
    props: {
        next: () => void,
        email: string, 
        setEmail: (email: string) => void,
        mitoAPI: MitoAPI
    }): JSX.Element => {

    // Make sure the input is focused on, as we want the experience of sign up
    // to be as fluid as possible, and the autofocus does not work for this 
    // input element, for some reason
    const emailInputRef = useRef<HTMLInputElement>(null);    
    useEffect(() => {
        emailInputRef.current?.focus()
    });

    const onSubmit = async (e: FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        await props.mitoAPI.sendSignUp(props.email);
        props.next();
    }

    return (
        <div className='signup-modal-left-column'>
            <div>
                <h1 className='mt-0'>
                    Sign Up for Mito
                </h1>
                <p className='signup-modal-text'>
                    We’ll send you periodic product updates and welcome any feedback. And no spam. Duh.
                </p>
            </div>
            <form className='signup-modal-email-form' onSubmit={onSubmit}>
                <h3 className='mb-20px'>
                    Your Email
                </h3>
                <input 
                    ref={emailInputRef}
                    className='input'
                    type='email'
                    value={props.email}
                    onChange={(event) => {props.setEmail(event.target.value)}}
                    placeholder='example@gmail.com' 
                    required
                    autoFocus
                />
                <button className='signup-modal-button-signup' type='submit'> Sign Up</button>  
            </form>
        </div>
    )
}


/* Step one requires the user to read the privacy policy */
const StepTwo = (
    props: {
        back: () => void;
        next: () => void;
    }): JSX.Element => {
    return (
        <div className='signup-modal-left-column'>
            <div>
                <h1 className='mt-0'>
                    Mito is Built for Privacy
                </h1>
                <p className='signup-modal-text'>
                    We make sure none of your private data leaves your computer. Read our CCPA compliant privacy policy <a href='https://privacy.trymito.io/privacy-policy' target='_blank' rel="noreferrer"><u>here</u></a>.
                </p>
            </div>
            <div className='signup-modal-buttons'>
                <button className='signup-modal-button-back' onClick={props.back}> Back</button> 
                <button className='signup-modal-button-next' onClick={props.next} autoFocus> Accept</button> 
            </div> 
        </div>
    )
}

export enum QuestionAnswers {
    PIVOT = 'Pivot',
    MERGE = 'Merge',
    COLUMN_FORMULAS = 'Column Formulas',
    EXPLORE_DATA = 'Explore Datasets',
    FILTER_SORT = 'Filter/Sort',
    NOT_SURE = 'I\'m Not Sure',
}

/* Step three asks the user want they want to use Mito for */
const StepThree = (
    props: {
        back: () => void;
        next: () => void;
        mitoAPI: MitoAPI;
    }): JSX.Element => {
    const [answers, setAnswers] = useState<QuestionAnswers[]>([])

    const InstallationQuestion = 'How was installation?';
    const [selectedFrustrationRating, setSelectedFrustrationRating] = useState<FrustrationRating | undefined>(undefined)

    // Takes an answer and either selects or unselects it
    const toggleAnswer = (answer: QuestionAnswers): void => {
        const newAnswers = [...answers];
        if (answers.includes(answer)) {
            newAnswers.splice(newAnswers.indexOf(answer), 1);
            setAnswers(newAnswers);
        } else {
            newAnswers.push(answer)
            setAnswers(newAnswers);
        }
    }

    const onSubmit = async () => {
        // Set the intended behavior
        await props.mitoAPI.sendIntendedBehavior(answers);
        // Set the feedback for installation
        await props.mitoAPI.sendFeedback({[InstallationQuestion]: selectedFrustrationRating})
        // Advance to the next step
        props.next();
    }

    return (
        <div className='signup-modal-left-column'>
            <div>
                <h3 className='mt-0 mb-5px'>
                    What are you looking to do with Mito?
                </h3>
                <div className='signup-modal-usage-grid'>
                    {Object.values(QuestionAnswers).map((answer) => {
                        const isSelected = answers.includes(answer as QuestionAnswers);

                        return (
                            <div 
                                className='signup-modal-usage-answer' 
                                style={{backgroundColor: isSelected ? 'pink' : 'white', border: isSelected ? '2px solid black' : '2px solid grey'}} 
                                key={answer} 
                                onClick={() => {toggleAnswer(answer as QuestionAnswers)}}
                            >
                                {answer}
                            </div>
                        )
                    })}
                </div>
                <h3 className='mt-5px mb-5px'>
                    How easy was installation?
                </h3>
                <FrustrationSelection
                    selectedFrustrationRating={selectedFrustrationRating}
                    setSelectedFrustrationRating={setSelectedFrustrationRating}
                    padding='2px 5px'
                />
            </div>
            <div className='signup-modal-buttons'>
                <button className='signup-modal-button-back' onClick={props.back}> Back</button> 
                <button className='signup-modal-button-next' onClick={onSubmit} autoFocus> Next</button> 
            </div>
        </div>
    )
}


/* 
    Main signup modal, which collects the users email, shows them the privacy policy, 
    and then asks them what they want to do with the tool.
*/
const SignupModal = (
    props: {
        setModal: (modalInfo: ModalInfo) => void;
        mitoAPI: MitoAPI;
    }): JSX.Element => {
    const [step, setStep] = useState(1);
    const [email, setEmail] = useState('');

    const next = () => {
        if (step + 1 > 3) {
            props.setModal({type: ModalEnum.None});
            void props.mitoAPI.sendLogMessage('finished_signup');
        } else {
            const newStep = Math.min(step + 1, 3);
            setStep(newStep)
            void props.mitoAPI.sendLogMessage('switched_signup_step', 
                {
                    'old_signup_step': step,
                    'new_signup_step': newStep
                }
            );
        }
    }
    const back = () => {
        const newStep = Math.max(step - 1, 0);
        setStep(newStep)

        void props.mitoAPI.sendLogMessage('switched_signup_step', 
            {
                'old_signup_step': step,
                'new_signup_step': newStep
            }
        );
    }   

    // Background colors of the different steps right column
    const backgroundColors: Record<number, string> = {
        1: '#FFEBEB',
        2: '#FFDAAE',
        3: '#F0C5BB',
    }

    return (
        <div className='overlay'>
            <div className='signup-modal-container'>
                <div className='signup-modal-left-column-container'>
                    {step === 1 &&
                        <StepOne
                            next={next}
                            email={email}
                            setEmail={setEmail}
                            mitoAPI={props.mitoAPI}
                        />
                    }
                    {step === 2 &&
                        <StepTwo
                            next={next}
                            back={back}
                        />
                    }
                    {step === 3 &&
                        <StepThree
                            next={next}
                            back={back}
                            mitoAPI={props.mitoAPI}
                        />
                    }
                    
                </div>
                <div className='signup-modal-right-column-container' style={{backgroundColor: backgroundColors[step]}}>
                    {step === 1 &&
                        <BlueMitoFolk/>
                    }
                    {step === 2 &&
                        <YellowMitoFolk/>
                    }
                    {step === 3 &&
                        <PinkMitoFolk/>
                    }
                </div>
            </div>
        </div>
    );
};

export default SignupModal;