import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-student-profile',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  template: `
    <div class="container">
      <h2>My Profile</h2>

      <form [formGroup]="profileForm" (ngSubmit)="onSubmit()" class="profile-form">

        <div class="field">
          <label for="name">Full Name *</label>
          <input id="name" type="text" formControlName="name" placeholder="Enter your name" />
          <span class="error" *ngIf="profileForm.get('name')?.touched && profileForm.get('name')?.invalid">
            Name is required.
          </span>
        </div>

        <div class="field">
          <label for="email">Email *</label>
          <input id="email" type="email" formControlName="email" placeholder="Enter your email" />
          <span class="error" *ngIf="profileForm.get('email')?.touched && profileForm.get('email')?.errors?.['required']">
            Email is required.
          </span>
          <span class="error" *ngIf="profileForm.get('email')?.touched && profileForm.get('email')?.errors?.['email']">
            Enter a valid email address.
          </span>
        </div>

        <div class="field">
          <label for="semester">Semester (1–8) *</label>
          <input id="semester" type="number" formControlName="semester" placeholder="Current semester" />
          <span class="error" *ngIf="profileForm.get('semester')?.touched && profileForm.get('semester')?.invalid">
            Semester must be between 1 and 8.
          </span>
        </div>

        <button type="submit" [disabled]="profileForm.invalid" class="submit-btn">
          Save Profile
        </button>

      </form>

      <div *ngIf="submitted" class="success-msg">
        ✅ Profile saved successfully!
      </div>
    </div>
  `,
  styles: [`
    .container { max-width:500px; margin:40px auto; padding:32px 24px; }
    h2 { color:#1a73e8; margin-bottom:24px; }
    .profile-form { background:white; padding:28px; border-radius:10px; border:1px solid #dde3f0; }
    .field { margin-bottom:20px; display:flex; flex-direction:column; gap:6px; }
    label { font-weight:bold; color:#333; font-size:0.9rem; }
    input { padding:10px; border:1px solid #ccc; border-radius:6px; font-size:1rem; }
    .error { color:#c5221f; font-size:0.82rem; }
    .submit-btn { width:100%; padding:12px; background:#1a73e8; color:white; border:none; border-radius:6px; font-size:1rem; cursor:pointer; }
    .submit-btn:disabled { background:#ccc; cursor:default; }
    .success-msg { margin-top:16px; background:#e6f4ea; border:1px solid #34a853; border-radius:8px; padding:14px; color:#1e7e34; }
  `]
})
export class StudentProfileComponent implements OnInit {
  profileForm!: FormGroup;
  submitted = false;

  constructor(private fb: FormBuilder) {}

  ngOnInit(): void {
    this.profileForm = this.fb.group({
      name:     ['', Validators.required],
      email:    ['', [Validators.required, Validators.email]],
      semester: ['', [Validators.required, Validators.min(1), Validators.max(8)]]
    });
  }

  onSubmit(): void {
    if (this.profileForm.valid) {
      console.log('Profile data:', this.profileForm.value);
      this.submitted = true;
    }
  }
}