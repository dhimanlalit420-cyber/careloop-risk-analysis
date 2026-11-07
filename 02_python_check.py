"""Reproduce the clinic-level appointment and no-show counts used in Part 2."""
import pandas as pd

appointments = pd.read_csv('appointments_clean.csv')
clinics = pd.read_csv('clinics_enriched.csv')
counts = (appointments.groupby('clinic_id')
          .agg(appointments=('no_show', 'size'), no_shows=('no_show', 'sum'))
          .reset_index()
          .merge(clinics[['clinic_id', 'clinic_name', 'city']], on='clinic_id', how='left'))
counts['no_show_pct'] = (100 * counts['no_shows'] / counts['appointments']).round(1)
print(counts[['clinic_name', 'city', 'appointments', 'no_shows', 'no_show_pct']]
      .sort_values('no_show_pct', ascending=False).to_string(index=False))

