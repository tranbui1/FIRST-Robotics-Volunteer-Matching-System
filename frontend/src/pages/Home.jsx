import './Home.css';
import { useNavigate } from 'react-router-dom';

function Home() {
    const navigate = useNavigate();

    const handleClick = () => {
        navigate('/match');
    }
    return (
        <div>
            <h1> FIRST Robotics Volunteer Page </h1>
            <div className="center">
                <p className="description">
                    Interested in volunteering but don't know where to start? <br />
                    Take our matching questionnaire to find out the most <br />
                    suitable roles for you! :)
                </p>
                <button className="button" type="button" onClick={handleClick}> 
                    Match me to a role! 
                </button>
            </div>
        </div>
    )

} export default Home;