import React, { useState } from 'react';
import Login from './Component/Login.jsx';
import PredictionForm from './Component/PredictionForm.jsx';



const App = () => {
  const [loggedIn, setLoggedIn] = useState(false);

  return (
    <>
   
      {!loggedIn ? (
        <Login onLogin={() => setLoggedIn(true)} /> 
      ) : (
        <PredictionForm />
      )}

   
    </>
  );
};

export default App;
