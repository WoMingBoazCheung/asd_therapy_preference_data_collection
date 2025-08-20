import React, { useState, useEffect, useRef } from 'react';
import SessionDisplay from './SessionDisplay';
import styles from './PoseViewer.module.css';

const PoseViewer = () => {
    const [session1, setSession1] = useState(null);
    const [session2, setSession2] = useState(null);
    const [frame, setFrame] = useState(0);
    const [isLoading, setIsLoading] = useState(true);
    const animationFrameId = useRef(null);

    const fetchSessions = async () => {
        setIsLoading(true);
        try {
            const response = await fetch('http://127.0.0.1:8000/session_pairs/get_session_pair/');
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            const data = await response.json();
            setSession1(data.session_1);
            setSession2(data.session_2);
            setFrame(0);
        } catch (error) {
            console.error("Error fetching session data:", error);
        } finally {
            setIsLoading(false);
        }
    };

    const handlePreferenceClick = async (preferred) => {
        if (!session1 || !session2) return;

        const comparisonData = {
            session_id_1: session1.name,
            session_id_2: session2.name,
            preferred: preferred,
        };

        try {
            const response = await fetch('http://127.0.0.1:8000/session_pairs/add_comparison/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(comparisonData),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(`HTTP error! status: ${response.status}, message: ${errorData.error}`);
            }
            
            console.log("Successfully saved preference.");
            fetchSessions();

        } catch (error) {
            console.error("Error saving preference:", error);
        }
    };

    useEffect(() => {
        const render = () => {
            setFrame(prevFrame => prevFrame + 1);
            animationFrameId.current = requestAnimationFrame(render);
        };
        animationFrameId.current = requestAnimationFrame(render);
        return () => cancelAnimationFrame(animationFrameId.current);
    }, []);

    useEffect(() => {
        fetchSessions();
    }, []);

    const session1WithFrame = session1 ? { ...session1, currentFrameData: session1.data[frame % session1.data.length] } : null;
    const session2WithFrame = session2 ? { ...session2, currentFrameData: session2.data[frame % session2.data.length] } : null;

    return (
        <div className={styles.container}>
            <div className={styles.controls}>
                <button onClick={fetchSessions} disabled={isLoading}>
                    {isLoading ? 'Loading...' : 'Load Different Sessions'}
                </button>
            </div>
            <div className={styles.sessionsWrapper}>
                <SessionDisplay session={session1WithFrame} sessionNumber={1} onPrefer={handlePreferenceClick} isLoading={isLoading} />
                <SessionDisplay session={session2WithFrame} sessionNumber={2} onPrefer={handlePreferenceClick} isLoading={isLoading} />
            </div>
        </div>
    );
};

export default PoseViewer;
