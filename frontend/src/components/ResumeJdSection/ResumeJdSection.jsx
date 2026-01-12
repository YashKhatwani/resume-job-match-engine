import React from 'react';
import './ResumeJdSection.css';

import JDInput from '../JDInput';
import { ResumeSection } from '../ResumeSection/ResumeSection';


export const ResumeJdSection = () => {
    return (
        <section className="resume-jd">
            <div className="columns">
                <div className="col left"><ResumeSection/></div>
                <div className="col right"><JDInput /></div>
            </div>

            <div className="controls">
                <button className="analyze">Analyze / Recalculate</button>
                <div className="sort">
                    Sort by:
                    <select aria-label="sort">
                        <option>Match %</option>
                        <option>Experience gap</option>
                    </select>
                </div>
            </div>
        </section>
    );
};
