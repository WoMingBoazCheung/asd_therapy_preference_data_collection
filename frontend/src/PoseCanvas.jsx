import React, { useRef, useEffect } from 'react';

const POSE_CONNECTIONS = [
    [1, 8], [1, 2], [1, 5], [2, 3], [3, 4], [5, 6], [6, 7],
    [8, 9], [9, 10], [10, 11], [8, 12], [12, 13], [13, 14],
    [1, 0], [0, 15], [15, 17], [0, 16], [16, 18],
    [11, 24], [11, 22], [22, 23], [14, 21], [14, 19], [19, 20]
];

const SKELETON_COLORS = ['#ff0000', '#00ff00', '#0000ff', '#ffff00', '#ff00ff', '#00ffff', '#ffffff'];

const drawSingleSkeleton = (ctx, keypoints, color) => {
    if (!keypoints || keypoints.length === 0) return;
    const keypointThreshold = 0.1;

    ctx.strokeStyle = color;
    ctx.lineWidth = 2;
    POSE_CONNECTIONS.forEach(([p1, p2]) => {
        const [x1, y1, c1] = [keypoints[p1 * 3], keypoints[p1 * 3 + 1], keypoints[p1 * 3 + 2]];
        const [x2, y2, c2] = [keypoints[p2 * 3], keypoints[p2 * 3 + 1], keypoints[p2 * 3 + 2]];
        if (c1 > keypointThreshold && c2 > keypointThreshold) {
            ctx.beginPath();
            ctx.moveTo(x1, y1);
            ctx.lineTo(x2, y2);
            ctx.stroke();
        }
    });

    ctx.fillStyle = color;
    for (let i = 0; i < keypoints.length; i += 3) {
        if (keypoints[i + 2] > keypointThreshold) {
            ctx.beginPath();
            ctx.arc(keypoints[i], keypoints[i + 1], 4, 0, 2 * Math.PI);
            ctx.fill();
        }
    }
};

const PoseCanvas = ({ frameData }) => {
    const canvasRef = useRef(null);

    useEffect(() => {
        const canvas = canvasRef.current;
        const ctx = canvas.getContext('2d');

        ctx.fillStyle = 'black';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        if (frameData && frameData.length > 0) {
            frameData.forEach(personData => {
                const { person_id, keypoints } = personData;
                const color = SKELETON_COLORS[person_id % SKELETON_COLORS.length];
                drawSingleSkeleton(ctx, keypoints, color);
            });
        }
    }, [frameData]); // Redraw only when frameData changes

    return <canvas ref={canvasRef} width="640" height="480" />;
};

export default PoseCanvas;
