import React, { useState } from "react";
import Header from "./components/Header/Header";
import "./App.css";
import "react-responsive-carousel/lib/styles/carousel.min.css"; // requires a loader
import { Carousel } from 'react-responsive-carousel';

function App() {
  return (
    <>
    <Header/>
    {/* <Carousel>
            <div>
              <img src="https://img.freepik.com/free-photo/morskie-oko-tatry_1204-510.jpg?t=st=1743259388~exp=1743262988~hmac=c38800eccdfe000513b5881be3eb723ecc4236cad8e4deb119f03197651860f2&w=2000" />
                  <p className="legend">Legend 1</p>
                </div>
                <div>
                    <img src="https://img.freepik.com/free-photo/morskie-oko-tatry_1204-510.jpg?t=st=1743259388~exp=1743262988~hmac=c38800eccdfe000513b5881be3eb723ecc4236cad8e4deb119f03197651860f2&w=2000" />
                    <p className="legend">Legend 2</p>
                </div>
                <div>
                    <img src="https://img.freepik.com/free-photo/morskie-oko-tatry_1204-510.jpg?t=st=1743259388~exp=1743262988~hmac=c38800eccdfe000513b5881be3eb723ecc4236cad8e4deb119f03197651860f2&w=2000" />
                    <p className="legend">Legend 3</p>
                </div>
      </Carousel> */}
    </>
  );
}

export default App;
