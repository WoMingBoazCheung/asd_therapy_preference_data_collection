import os
import json
import numpy as np
from django.core.management.base import BaseCommand
from session_pairs.models import Session

# --- Person Tracking Logic (adapted from OpenPoseParser) ---

MIN_CONFIDENCE = 0.3
TRACKING_THRESHOLD = 30.0
KEYPOINT_NAMES_COUNT = 25

def pose_distance(keypoints1, keypoints2):
    """Calculate the average distance between two sets of keypoints."""
    total_dist = 0
    count = 0
    for i in range(0, KEYPOINT_NAMES_COUNT * 3, 3):
        # Check confidence scores (c1 and c2)
        c1 = keypoints1[i + 2]
        c2 = keypoints2[i + 2]
        if c1 > MIN_CONFIDENCE and c2 > MIN_CONFIDENCE:
            dx = keypoints1[i] - keypoints2[i]
            dy = keypoints1[i + 1] - keypoints2[i + 1]
            total_dist += np.sqrt(dx * dx + dy * dy)
            count += 1
    return total_dist / count if count > 0 else float("inf")

# --- End of Tracking Logic ---

class Command(BaseCommand):
    help = 'Scans the sample_data directory and populates the Session model with tracked keypoint data.'

    def handle(self, *args, **options):
        sample_data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../../sample_data'))
        self.stdout.write(f'Scanning directory: {sample_data_dir}')

        try:
            sessions_in_dir = {d for d in os.listdir(sample_data_dir) if os.path.isdir(os.path.join(sample_data_dir, d))}
            self.stdout.write(f'Found {len(sessions_in_dir)} directories.')

            for session_name in sessions_in_dir:
                # --- Reset tracking for each new session ---
                next_person_id = 0
                previous_poses = [] # This will store poses from the last frame
                # -------------------------------------------

                session_dir_path = os.path.join(sample_data_dir, session_name)
                session_frames_data = []
                
                json_files = sorted([f for f in os.listdir(session_dir_path) if f.endswith('.json')])

                for filename in json_files:
                    file_path = os.path.join(session_dir_path, filename)
                    current_poses = []
                    try:
                        with open(file_path, 'r') as f:
                            data = json.load(f)
                            if data.get('people'):
                                for person_data in data['people']:
                                    keypoints = person_data.get('pose_keypoints_2d', [])
                                    if keypoints:
                                        # Create a temporary pose object for tracking
                                        current_poses.append({"keypoints": keypoints, "person_id": None})
                    except (json.JSONDecodeError, IOError) as e:
                        self.stderr.write(self.style.ERROR(f'Error processing {file_path}: {e}'))

                    # --- Assign Tracked IDs --- 
                    for current_pose in current_poses:
                        best_match = None
                        best_distance = float("inf")
                        for prev_pose in previous_poses:
                            dist = pose_distance(current_pose["keypoints"], prev_pose["keypoints"])
                            if dist < best_distance:
                                best_distance = dist
                                best_match = prev_pose
                        
                        if best_match and best_distance < TRACKING_THRESHOLD:
                            current_pose["person_id"] = best_match["person_id"]
                        else:
                            current_pose["person_id"] = next_person_id
                            next_person_id += 1
                    # --------------------------

                    # Store the frame data with assigned IDs
                    session_frames_data.append(current_poses)
                    # Update previous_poses for the next frame
                    previous_poses = current_poses

                # Update or create the session object with the tracked data
                session, created = Session.objects.update_or_create(
                    name=session_name,
                    defaults={'data': session_frames_data}
                )
                status = "Created" if created else "Updated"
                self.stdout.write(f'{status} session: {session_name} with {len(session_frames_data)} frames.')

            # Remove old sessions
            sessions_in_db = set(Session.objects.values_list('name', flat=True))
            old_sessions = sessions_in_db - sessions_in_dir
            if old_sessions:
                count, _ = Session.objects.filter(name__in=old_sessions).delete()
                self.stdout.write(self.style.SUCCESS(f'Removed {count} old sessions.'))

            self.stdout.write(self.style.SUCCESS('Session database is now up to date with tracked IDs.'))

        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f'Directory not found: {sample_data_dir}'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'An unexpected error occurred: {e}'))