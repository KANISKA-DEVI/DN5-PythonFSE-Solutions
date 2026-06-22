import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';

export interface Course {
  id: number;
  name: string;
  code: string;
  credits: number;
  grade: string;
}

@Injectable({ providedIn: 'root' })
export class CourseService {
  getCourses(): Observable<Course[]> {
    const courses: Course[] = [
      { id: 1, name: 'Data Structures & Algorithms', code: 'CS101', credits: 4, grade: 'A' },
      { id: 2, name: 'Database Management Systems',  code: 'CS102', credits: 3, grade: 'B' },
      { id: 3, name: 'Object Oriented Programming',  code: 'CS103', credits: 4, grade: 'A' },
      { id: 4, name: 'Circuit Theory',               code: 'EC101', credits: 3, grade: 'B' },
      { id: 5, name: 'Thermodynamics',               code: 'ME101', credits: 3, grade: 'C' },
    ];
    return of(courses);
  }
}