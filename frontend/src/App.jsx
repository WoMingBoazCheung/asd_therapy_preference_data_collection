import React from 'react';
import PoseViewer from './PoseViewer';
import styles from './App.module.css'; // Import the CSS module

function App() {
    return (
        <div className={styles.App}>
            <header className={styles.AppHeader}>
                <h1>ASD Therapy Session Comparison</h1>
            </header>
            <main>
                <PoseViewer />
            </main>
        </div>
    );
}

export default App;
