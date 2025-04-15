import React from 'react';
import './AQIScale.css';

const AQIScale = ({ aqi }) => {
  const getPosition = () => {
    const ranges = [
      { max: 50, pos: 8 },
      { max: 100, pos: 23 },
      { max: 150, pos: 38 },
      { max: 200, pos: 53 },
      { max: 300, pos: 75 },
      { max: Infinity, pos: 95 }
    ];

    for (let i = 0; i < ranges.length; i++) {
      if (aqi <= ranges[i].max) return `${ranges[i].pos}%`;
    }
    return '0%';
  };

  const getCategory = () => {
    if (aqi <= 50) return 'Good';
    if (aqi <= 100) return 'Moderate';
    if (aqi <= 150) return 'Poor';
    if (aqi <= 200) return 'Unhealthy';
    if (aqi <= 300) return 'Severe';
    return 'Hazardous';
  };

  return (
    <div className="aqi-scale-wrapper">
      <h3 className="aqi-title">Air Quality Index (AQI): <span className={`aqi-text ${getCategory().toLowerCase()}`}>{aqi} - {getCategory()}</span></h3>

      <div className="aqi-bar">
        <div className="aqi-gradient"></div>
        <div className="aqi-indicator" style={{ left: getPosition() }}>
          <div className="indicator-tooltip">{aqi}</div>
        </div>
      </div>

      <div className="aqi-labels">
        <span>0</span><span>50</span><span>100</span><span>150</span><span>200</span><span>300</span><span>301+</span>
      </div>

      <div className="aqi-categories">
        {['Good', 'Moderate', 'Poor', 'Unhealthy', 'Severe', 'Hazardous'].map((cat) => (
          <span
            key={cat}
            className={`aqi-category ${getCategory() === cat ? 'active' : ''}`}
          >
            {cat}
          </span>
        ))}
      </div>
    </div>
  );
};

export default AQIScale;
