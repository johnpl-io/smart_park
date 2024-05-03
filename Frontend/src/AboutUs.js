import React from 'react';
import './AboutUs.css';

function AboutUs() {
  return (
    <div className="about-us-container">
      <h1>Welcome to Smart Park</h1>
      <p className="about-us-description">
        At Smart Park, we believe that finding parking shouldn't be a hassle. Our mission is to simplify your parking experience by providing a seamless platform where you can effortlessly locate parking spots near you, saving you time and frustration. Whether you're heading to a busy downtown area, a crowded event, or simply exploring a new city, Smart Park is your trusted companion for stress-free parking.
      </p>

      <h2>Why Choose Smart Park?</h2>
      <ul className="why-choose-list">
        <li><strong>Convenience:</strong> With just a few taps, you can discover available parking options in real-time, eliminating the need to circle the block endlessly in search of a spot.</li>
        <li><strong>Accessibility:</strong> Our user-friendly interface is designed to be accessible to everyone, ensuring that finding parking is effortless for users of all backgrounds and abilities.</li>
        <li><strong>Reliability:</strong> Say goodbye to the uncertainty of parking availability. Smart Park provides up-to-date information on parking availability, so you can plan your journey with confidence.</li>
        <li><strong>Safety:</strong> We prioritize your safety and security. Smart Park only partners with trusted parking providers, giving you peace of mind when you park with us.</li>
      </ul>

      <h2>Our Vision</h2>
      <p className="our-vision">
        At Smart Park, we envision a future where parking is no longer a source of stress and frustration. By harnessing the power of technology, we aim to revolutionize the way people park, making it simpler, more convenient, and more enjoyable for everyone.
      </p>

      <h2>Get Started Today</h2>
      <p className="get-started">
        Ready to experience the convenience of Smart Park for yourself? Download our app or visit our website to start finding parking spots near you. Say goodbye to parking headaches and hello to hassle-free parking with Smart Park.
      </p>

      <p className="join-us">
        Join us on our journey to redefine parking and make urban mobility smarter, one parking spot at a time. Welcome to Smart Park – where parking meets convenience.
      </p>
    </div>
  );
}

export default AboutUs;
