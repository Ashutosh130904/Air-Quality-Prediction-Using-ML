import React, { useState } from "react";
import "./PredictionForm.css";
import AQIScale from './AQIScale.jsx';
import BoyStatus from "./BoyStatus.jsx";
import Header from "./Header.jsx";
import NavBar from "./NavBar.jsx";


function PredictionForm() {
  const [formData, setFormData] = useState({
    pm25: "", // PM2.5 (µg/m³)
    pm10: "", // PM10 (µg/m³)
    no: "", // NO (µg/m³)
    no2: "", // NO2 (µg/m³)
    nox: "", // NOx (ppb)
    nh3: "", // NH3 (µg/m³)
    so2: "", // SO2 (µg/m³)
    co: "", // CO (mg/m³)
    ozone: "", // Ozone (µg/m³)
    benzene: "", // Benzene (µg/m³)
  });

  const [prediction, setPrediction] = useState("");

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch("http://localhost:5000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });

      const data = await response.json();
      setPrediction(data.prediction);
    } catch (error) {
      console.error("Error:", error);
    }
  };


  return (
  <>
  <Header/>
    <div className="main-container">
      <h1 className="main-title"> 🌿 Input some polutants to predict the AQI value </h1>
      <form onSubmit={handleSubmit} className="form-card">
  <div className="input-group">
    <label className="input-label">PM2.5 (µg/m³)</label>
    <input type="number" name="pm25" value={formData.pm25} onChange={handleChange} required className="form-input" placeholder="Enter PM2.5 value" />
  </div>
  
  <div className="input-group">
    <label className="input-label">PM10 (µg/m³)</label>
    <input type="number" name="pm10" value={formData.pm10} onChange={handleChange} required className="form-input" placeholder="Enter PM10 value" />
  </div>


  <div className="input-group">
    <label className="input-label">NO2 (µg/m³)</label>
    <input type="number" name="no2" value={formData.no2} onChange={handleChange} required className="form-input" placeholder="Enter NO2 value" />
  </div>



  <div className="input-group">
    <label className="input-label">NH3 (µg/m³)</label>
    <input type="number" name="nh3" value={formData.nh3} onChange={handleChange} required className="form-input" placeholder="Enter NH3 value" />
  </div>

  <div className="input-group">
    <label className="input-label">SO2 (µg/m³)</label>
    <input type="number" name="so2" value={formData.so2} onChange={handleChange} required className="form-input" placeholder="Enter SO2 value" />
  </div>

  <div className="input-group">
    <label className="input-label">CO (mg/m³)</label>
    <input type="number" name="co" value={formData.co} onChange={handleChange} required className="form-input" placeholder="Enter CO value" />
  </div>

  <div className="input-group">
    <label className="input-label">Ozone (µg/m³)</label>
    <input type="number" name="ozone" value={formData.ozone} onChange={handleChange} required className="form-input" placeholder="Enter Ozone value" />
  </div>


  <button type="submit" className="submit-btn">
    🔍 Predict
  </button>
</form>


      {prediction && (
        <div className="prediction-card">
          <h2 className="prediction-heading">🔍 Prediction Result</h2>
          <p className="prediction-text">
            <span className="prediction-badge">{prediction}</span>
          </p>
        </div>
      )}

      <AQIScale aqi={prediction} />

      <BoyStatus aqi={prediction} />

      <NavBar/>

    </div>
    </>
  );
}

export default PredictionForm;