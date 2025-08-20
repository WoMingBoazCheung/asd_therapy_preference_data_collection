import React from 'react';
import PoseCanvas from './PoseCanvas';
import styles from './SessionDisplay.module.css';

const SessionDisplay = ({ session, sessionNumber, onPrefer, isLoading }) => {
    if (!session) {
        return (
            <div className={styles.container}>
                <h3>Session {sessionNumber}</h3>
                <div className={styles.canvasPlaceholder}>
                    <p>Loading...</p>
                </div>
                <button className={styles.preferenceButton} disabled>Prefer Session {sessionNumber}</button>
            </div>
        );
    }

    return (
        <div className={styles.container}>
            <h3>{session.name}</h3>
            <PoseCanvas frameData={session.currentFrameData} />
            <button className={styles.preferenceButton} onClick={() => onPrefer(sessionNumber)} disabled={isLoading}>
                Prefer Session {sessionNumber}
            </button>
        </div>
    );
};

export default SessionDisplay;