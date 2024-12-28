import React from 'react';
import { Routes, Route } from 'react-router-dom';
import SignUp from './component/Signup';
import SignIn from './component/SignIn';
import FloorMapComponent from './component/FloorMapComponent';

const App = () => {
  return (
    <Routes>
  <Route path="/" element={<SignIn />} />
  <Route path="/signup" element={<SignUp />} />
  <Route path="/FloorMapComponent" element={<FloorMapComponent />} />
</Routes>
  );
};

//export default App;

// import React from 'react';
// import FloorMapComponent from './component/FloorMapComponent';
// import SignUp from './component/Signup';
// import SignIn from './component/SignIn';

// const App = () => {
//   return (
//     <div>
//       <h1>Hospital Map</h1>
//       <FloorMapComponent />
//     </div>
//   );
// };

export default App;

