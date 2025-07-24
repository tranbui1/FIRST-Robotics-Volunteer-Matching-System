import './Questionnaire.css';
import { useState, useEffect } from 'react';

/*
Agenda: parse answer options:
    1. drop down
*/

const AgeDropDown = () => {
    // Make an array containing age groups from 11 - 100
    const ages = [];

    for (let i = 11; i <= 100 ; i++) {
        ages.push(i);
    }

    return (
        <select id="age">
            {ages.map(age => (
                <option className="option"> {age} </option>
            ))}
        </select>
    );
}

const RenderContent = (data, type, handleAnswerClick) => {
    if (type === "number") {
        // return a number selector jsx element
    } else if (type === "select-2") {
        return (
            <div className="button-container center">
                <button className="button" onClick={handleAnswerClick}>
                    {data.options[0]}
                </button>
                <button className="button" onClick={handleAnswerClick}>
                    {data.options[1]}
                </button>
            </div>
        )
    } else if (type === "select-3") {
        return (
            <div className="button-container-3 center">
                <button className="button button-select-3"> Yes</button>
                <button className="button button-select-3"> No</button>
                <button className="button button-select-3"> No Preference</button>
            </div>
        )
    } else if (type === "multiselect") {
        // return a multiselect element
    }
}



function Questionnaire() {
    const [questionId, setQuestionId] = useState(0);
    const [data, setData] = useState(null);

    const fetchData = async () => {
        const response = await fetch(`http://127.0.0.1:5000/api/get-question?question_id=${questionId}`);
        const result = await response.json();
        setData(result);
    };

    const handleAnswerClick = () => {
        setQuestionId(prev => prev + 1); // Only increment when user clicks
    };

    useEffect(() => {
        fetchData();
    }, [questionId]); // Refetch when questionId changes

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
            <h2 className="exit"> × Exit</h2>
            <img className="logo" src="/images/logo.png" alt="FIRST Robotics logo" />
            <h2 className="logo-text"> FIRST Robotics </h2>
        </div>
            <h1 className="center question">
                {data ? data.question : 'Loading...'}
            </h1>
            <p className="center description"> Insert description here: lorum ipsum or something</p>
            {/* {data ? renderContent(data, data.type, handleAnswerClick) : "Loading"} */}

            <div className="age-container">
                <AgeDropDown />
            </div>

            <div className="navigation">
                {/* Conditionally renders next and back navigation */}
                {questionId > -1 && ( /* Set to -1 for development purposes */
                    <h2 className="navigation-button"> Next → </h2>
                )}

                {questionId < 10 && (
                    <h2 className="navigation-button"> ← Back </h2>
                )}
            </div>
        </div>
    );
}

export default Questionnaire;