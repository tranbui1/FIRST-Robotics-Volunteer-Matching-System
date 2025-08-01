import './Questionnaire.css';
import { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';

/* Agenda:
    1. change size of lettering based on question length
    2. work on the rest of the days, little pref, etc.
    3. placeholder for number of days for now
    5. make the 2 buttons width larger
*/

const CustomDropDown = ({ prompt, options }) => {
    const [isOpen, setIsOpen] = useState(false);
    const [choice, setChoice] = useState(null);

    // Ref for detecting outside click
    const dropdownRef = useRef(null);
    const buttonRef = useRef(null);

    // Close dropdown when clicking outside
    useEffect(() => {
        const handleClickOutside = (event) => {
            if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
                setIsOpen(false);
            }
        };

        document.addEventListener('mousedown', handleClickOutside);
        return () => {
            document.removeEventListener('mousedown', handleClickOutside);
        };
    }, []);

    // Dynamically adjust the height gap between the navigation and dropdown button
    useEffect(() => {
        if (buttonRef.current) {
            const buttonHeight = buttonRef.current.offsetHeight;
            const navigation = document.querySelector('.navigation');

            if (navigation) {
                const baseOffset = 25; 
                const adjustment = buttonHeight * 0.5; 
                navigation.style.top = `calc(${baseOffset}vh - ${adjustment}px)`;
            }
        }
    }, [choice]);

    return (
        <div className="custom-dropdown" ref={dropdownRef}>
            <button ref={buttonRef} onClick={() => setIsOpen(!isOpen)} aria-expanded={isOpen}> 
                <span className="custom-dropdown-text">{choice || prompt}</span>
                <span className="arrow">▼</span>
            </button>
            {isOpen && (
                <ul>
                    {options.map(option => (
                        <li key={option} onClick={() => {setChoice(option); setIsOpen(false);}}>
                            {option}
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
}

const AgeDropDown = () => {
    const ages = Array.from({ length: 88 }, (_, i) => i + 13);
    
    return <CustomDropDown prompt={"Select your age"} options={ages} />;
}

const MultiChoiceDropDown = ({ prompt, options }) => {
    const [isOpen, setIsOpen] = useState(false);
    const [choice, setChoice] = useState([]);
    const buttonRef = useRef(null);
    const dropDownRef = useRef(null);

    // Close dropdown when clicking outside
    useEffect(() => {
        const handleClickOutside = (event) => {
            if (dropDownRef.current && !dropDownRef.current.contains(event.target)) {
                setIsOpen(false);
            }
        };

        document.addEventListener('mousedown', handleClickOutside);
        return () => {
            document.removeEventListener('mousedown', handleClickOutside);
        };
    }, []);

    const handleRemoveOnClick = (event) => {
        event.stopPropagation();
        const clickedItem = event.target;
        const clickedItemText = clickedItem.textContent.replace(/\s*×\s*$/, '').trim();
        setChoice(choice.filter((item) => item !== clickedItemText));
    }

    const handleClick = (event) => {
        handleRemoveOnClick(event);
    }

    // Dynamically adjust the height gap between the navigation and dropdown button
    useEffect(() => {
        if (buttonRef.current) {
            const buttonHeight = buttonRef.current.offsetHeight;
            const navigation = document.querySelector('.navigation');

            if (navigation) {
                const baseOffset = 25; 
                const adjustment = buttonHeight * 0.5; 
                navigation.style.top = `calc(${baseOffset}vh - ${adjustment}px)`;
            }
        }
    }, [choice]);

    return (
        <div className="custom-dropdown" ref={dropDownRef}>
            <button onClick={() => setIsOpen(!isOpen)} aria-expanded={isOpen} ref={buttonRef}> 
                <span className="custom-dropdown-text"> 
                    {!choice.length == -0 ? "" : prompt}
                </span>
                <div className={`selected-container ${choice.length === 1 ? 'single-item' : ''}`}> 
                    {choice.length > 0 
                    ? choice.map(item => (
                        <span key={item} onClick={handleClick} className="selected"> {`${item}  ×`} </span>
                    ))
                    : ""}
                </div>
                <span className="arrow">▼</span>
            </button>
            {isOpen && (
                <ul>
                    {options.map(option => (
                        <li className={`multi-choice ${choice.includes(option) ? 'delete' : ''}`} 
                            key={option} onClick={() => {setChoice(prev => [...prev, option])}}>
                            {option}
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
}

const RenderContent = ({ data, button, setSelectedButton }) => {
    const handleButtonClick = (event) => {
        setSelectedButton(event.target.id);
    }

    if (data.type == "number-age") {
        return <AgeDropDown />; 
    } else if (data.type == "number-days") {
        // TODO: implement, placeholder for now
        return <AgeDropDown />; 
    } else if (data.type == "select-2") {
        return (
            <div className="button-container-2 center">
                <button id="button1" className={`button ${button == "button1" ? "selected-button" : ""}`} onClick={handleButtonClick}>
                    {data.options[0]}
                </button>
                <button id="button2" className={`button ${button == "button2" ? "selected-button" : ""}`} onClick={handleButtonClick}>
                    {data.options[1]}
                </button>
            </div>
        );
    } else if (data.type == "select-3") {
        return (
            <div className="button-container-3 center">
                <button id="button1" className={`button button-select-3 ${button == "button1" ? "selected-button" : ""}`} onClick={handleButtonClick}> 
                    {data.options[0]}
                </button>
                <button id="button2" className={`button button-select-3 ${button == "button2" ? "selected-button" : ""}`} onClick={handleButtonClick}> 
                    {data.options[1]}
                </button>
                <button id="button3" className={`button button-select-3 ${button == "button3" ? "selected-button" : ""}`} onClick={handleButtonClick}> 
                    {data.options[2]}
                </button>
            </div>
        );
    } else if (data.type == "multiselect") {
        return <MultiChoiceDropDown prompt={data.prompt} options={data.options} />; 
    } else if (data.type == "custom-dropdown") {
        return <CustomDropDown prompt={data.prompt} options={data.options} />;
    }
}

const Modal = ({ isModalOpen, setModalOpen }) => {
    let navigate = useNavigate();

    return (
        <div className="modal-overlay">
            <div className="modal-content"> 
                <p className="modal-header"> Exit Questionnaire? </p>
                <p className="modal-text"> Are you sure you want to exit this quiz? <br /> Your progress will not
                    be saved.
                </p>
                <div className="modal-buttons"> 
                    <button className="button gray" onClick={() => setModalOpen(false)}> Cancel </button>
                    <button className="button red" onClick={() => navigate('/')}> Exit </button>
                </div>
            </div>
        </div>
    )
}

function Questionnaire() {
    const [questionId, setQuestionId] = useState(0);
    const [data, setData] = useState(null);
    const [isModalOpen, setModalOpen] = useState(false);
    const [button, setSelectedButton] = useState(null);
    let navigate = useNavigate();


    const fetchData = async () => {
        const response = await fetch(`http://127.0.0.1:5000/api/get-question?question_id=${questionId}`);
        const result = await response.json();
        setData(result);
    };

    const handleNextAnswerClick = () => {
        setQuestionId(prev => prev + 1); 
    };

    const handleBackAnswerClick = () => {
        setQuestionId(prev => prev - 1); 
    };

    useEffect(() => {
        fetchData();
    }, [questionId]); 

    // Dynamically changes the size of questions based on length
    useEffect(() => {
        if (data) {
            const questionLen = data.question.length;
            const question = document.querySelector('.question');
            
            if (question) {
                const baseFontSize = 6;   
                const minFontSize = 2;   
                const scaleFactor = Math.max(minFontSize, baseFontSize - (questionLen / 25));
                
                question.style.fontSize = `${scaleFactor}vmax`;
            }
        }
    }, [data]);

    return (
        <div
            id="disable-copy"
            className="flat background"
            style={{backgroundImage: 'url(/images/background.jpg)'}}
        >   
        <div> 
            <progress value={0.6}/>
        </div>
        <div className="header">
            <h2 className="exit" onClick={() => setModalOpen(true)}> × Exit</h2>
            <img className="logo" src="/images/logo.png" alt="FIRST Robotics logo" />
        </div>
            <h1 className="center question">
                {data ? data.question : 'Loading...'}
            </h1>
            <p className="center description"> Insert description here</p>

            {data ? <RenderContent data={data} button={button} setSelectedButton={setSelectedButton}/> : "Loading"}

            {isModalOpen && 
                <div>
                    <Modal isModalOpen={isModalOpen} setModalOpen={setModalOpen}/>
                </div>
            }        

            <div className={`navigation ${isModalOpen ? "disabled" : ""}`}>
                {/* Conditionally renders next and back navigation */}
                {questionId < 10 && ( 
                    <h2 className="navigation-button" onClick={() => {handleNextAnswerClick(); setSelectedButton(null);}}> Next → </h2>
                )}
                {questionId > 0 && (
                    <h2 className="navigation-button" onClick={() => {handleNextAnswerClick(); setSelectedButton(null);}}> ← Back </h2>
                )}
            </div>
        </div>
    );
}

export default Questionnaire;