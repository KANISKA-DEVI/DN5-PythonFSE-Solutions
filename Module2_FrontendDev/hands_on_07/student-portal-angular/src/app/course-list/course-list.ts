import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { CourseService, Course } from '../course';
import { CourseCardComponent } from '../course-card/course-card';

@Component({
  selector: 'app-course-list',
  standalone: true,
  imports: [CommonModule, FormsModule, CourseCardComponent],
  template: `
    <div class="container">
      <h2>Available Courses</h2>

      <input
        type="text"
        placeholder="Search courses..."
        [(ngModel)]="searchTerm"
        class="search-input"
      />

      <div *ngIf="loading" class="loading">Loading courses...</div>

      <div class="grid" *ngIf="!loading">
        <app-course-card
          *ngFor="let course of filteredCourses; trackBy: trackById"
          [name]="course.name"
          [code]="course.code"
          [credits]="course.credits"
          [grade]="course.grade"
        ></app-course-card>
      </div>

      <p *ngIf="!loading && filteredCourses.length === 0" class="no-results">
        No courses found.
      </p>
    </div>
  `,
  styles: [`
    .container { max-width:1100px; margin:0 auto; padding:32px 24px; }
    h2 { color:#1a73e8; margin-bottom:20px; }
    .search-input { padding:10px 16px; width:100%; max-width:400px; border:1px solid #ccc; border-radius:6px; margin-bottom:24px; font-size:1rem; }
    .grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(260px,1fr)); gap:20px; }
    .loading { color:#1a73e8; font-style:italic; }
    .no-results { color:#999; }
  `]
})
export class CourseListComponent implements OnInit {
  courses: Course[]  = [];
  searchTerm: string = '';
  loading: boolean   = true;

  constructor(private courseService: CourseService) {}

  ngOnInit(): void {
    this.courseService.getCourses().subscribe({
      next: (data) => { this.courses = data; this.loading = false; },
      error: (err)  => { console.error('Error:', err); this.loading = false; }
    });
  }

  get filteredCourses(): Course[] {
    return this.courses.filter(c =>
      c.name.toLowerCase().includes(this.searchTerm.toLowerCase())
    );
  }

  trackById(index: number, course: Course): number {
    return course.id;
  }
}