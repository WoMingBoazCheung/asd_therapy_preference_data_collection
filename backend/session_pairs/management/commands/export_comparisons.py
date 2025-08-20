import os
import pandas as pd
from django.core.management.base import BaseCommand
from session_pairs.models import SessionComparison

class Command(BaseCommand):
    help = 'Exports the SessionComparison model data to a CSV file.'

    def handle(self, *args, **options):
        output_folder = 'csv_output'
        output_filename = 'session_comparisons_from_django.csv'
        
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
            self.stdout.write(f"Created directory: {output_folder}")

        output_path = os.path.join(output_folder, output_filename)

        queryset = SessionComparison.objects.all().values('session_id_1', 'session_id_2', 'preferred')
        
        if not queryset.exists():
            self.stdout.write("No comparisons in the database to export.")
            return

        try:
            df = pd.DataFrame(list(queryset))
            df.to_csv(output_path, index=False)
            self.stdout.write(self.style.SUCCESS(f"Successfully exported {len(df)} comparisons to {output_path}"))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"An error occurred during CSV export: {e}"))
