# this variable is the data of the earthquake safety page
safe_html = '''
<style>
.tips-intro {
    margin-bottom: 40px;
}
.tips-locations {
    margin-bottom: 60px;
}
.tips-preparations {
    margin-bottom: 60px;
}
.emergency-kit {
    margin-bottom: 60px;
}
.tips-secondary-info {
    margin-bottom: 60px;
}
.tips-medical {
    margin-bottom: 60px;
}
h2 {
    color: #FF473A;
    margin-top: 40px;
}
h3 {
    color: #228B22;
}
</style>
        <div className="tips-container">
            <div className="tips-intro">
                <p class="lead">About 20,000 earthquakes occur every year. They can happen at any moment, so it's important to plan accordingly and be prepared for an earthquake at any moment or place.</p>
            </div>
            <div className="tips-locations">
                <h2>I. What to do, when an earthquake starts near you?</h2>
                <h3>Indoors</h3>
                <p>While indoors during an earthquake, the optimal thing to do is to find a safe spot away from windows and preferably on the first floor. Then you would need to get into the "drop, cover, and hold position". This procedure is basically dropping to your knees, finding a safe spot for cover such as a table, and then covering your head with your hands and placing it in your lap.</p>
                <h3>Outdoors</h3>
                <p>If an earthquake begins while you are outdoors, do not try to run inside. Injury can occur from nearby broken doorways and windows. Instead look for an open area away from powerlines, buildings, and anything else that could be flung around during an earthquake. Get into the drop and cover position and wait out the shaking.</p>
                <h3>Driving</h3>
                <p>While in a vehicle during an earthquake, drive to an area free of powerlines, overpasses or anything else that could fall during the quake. Stay buckled and remain in the car until the quake has ended. Once it has ended check the vehicle for damage as well as any roadways.</p>
            </div>
            <div className="tips-preparation">
                <h2>II. Earthquake Preparation Tips</h2>
                <div className="emergency-kit">
                    <h3>Keep an emergency kit</h3>
                    <p>An emergency kit can save the day should the worst ocur during an earthquake. Consider leaving a kit in your house, car, or bring one in your luggage should you find yourself in an earthquake prone area. Your emergency kit should include (but not be limited to):</p>
                    <ul className="tips-emergency-kit">
                        <li>Bandages</li>
                        <li>Gauze</li>
                        <li>Antiseptic</li>
                        <li>Pain relievers (ibuprofen, aspirin)</li>
                        <li>Space blanket</li>
                        <li>Dust mask</li>
                        <li>Flashlight</li>
                        <li>Some type of whistle or noise maker to call for help</li>
                        <li>bottled water</li>
                        <li>canned food</li>
                    </ul>
                    <p>It is recommended to have three days of non-perishable food and water. If traveling abroad try to bring as much as you can fit.</p>
                </div>
                <div className="tips-secondary-info">
                    <h3>Sign up for STEP and Quake</h3>
                    <p>Sign up for the Smart Traveler Enrollment Program, or STEP, through the Bureau of Consular Affairs. This will send you important emergency information during a disaster. Also consider signing up here at Quake for even more information!</p>

                    <h3>Other Info</h3>
                    <ul>
                        <li>Consider purchasing travel insurance to cover possible expenses should an earthquake occur abroad</li>
                        <li>Try to bring cash and copies of important travel documents incase you need to evacuate a country</li>
                    </ul>
                    <h2>III. If you're caught in an earthquake </h2>
                    <h3>Signaling for help</h3>
                    <p>During an earthquake, becoming buried under debri is a possibility so you may want to learn how to signal for help so rescuers can find you.</p>
                    <p>Possible signaling techniques</p>
                    <ul className="tips-signaling">
                        <li>Blowing on your whistle in bursts of three until help arrives</li>
                        <li>Flicking a light on and off until help arrives</li>
                        <li>Shining a flashlight if in a dark area</li>
                        <li>Yelling loudly</li>
                        <li>Tapping on piping or other objects that may carry sound</li>
                    </ul>
                    <h3>Medical Info</h3>
                    <p>Should you ever find yourself or someone near you injured in an earthquake, refer to these links for medical information.</p>
                    <ul className="tips-medical-links">
                        <li><a href="https://www.mayoclinic.org/first-aid" target="_blank">Mayo Clinic</a></li>
                    </ul>
                </div>
            </div>
        </div>
'''
