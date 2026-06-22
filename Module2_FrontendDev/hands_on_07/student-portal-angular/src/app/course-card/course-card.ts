import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Course } from '../course';

@Component({
  selector: 'app-course-card',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="card">
      <span class="grade">{{ grade }}</span>
      <h3>{{ name }}</h3>
      <p>{{ code }}</p>
      <span class="credits">{{ credits }} Credits</span>
    </div>
  `,
  styles: [`
    .card { background:white; border:1px solid #dde3f0; border-radius:10px; padding:20px; box-shadow:0 2px 8px rgba(0,0,0,0.07); }
    h3 { color:#1a73e8; margin-bottom:8px; }
    p { color:#666; font-size:0.9rem; margin-bottom:12px; }
    .grade { float:right; background:#34a853; color:white; border-radius:20px; padding:3px 10px; font-size:0.8rem; }
    .credits { background:#e8f0fe; color:#1a73e8; border-radius:20px; padding:3px 10px; font-size:0.8rem; font-weight:bold; }
  `]
})
export class CourseCardComponent {
  @Input() name: string    = '';
  @Input() code: string    = '';
  @Input() credits: number = 0;
  @Input() grade: string   = '';
}