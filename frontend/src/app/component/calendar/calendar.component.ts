import { Component, EventEmitter, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TranslateModule } from '@ngx-translate/core';

@Component({
  selector: 'app-calendar',
  standalone: true,
  imports: [CommonModule, TranslateModule],
  templateUrl: './calendar.component.html',
  styleUrl: './calendar.component.css'
})
export class CalendarComponent {
  @Output() selectDate = new EventEmitter<Date | null>()

  currentDate: Date = new Date();
  daysInMonth: Array<number | null> = [];
  currentMonth: string = '';
  currentYear: number = 0;
  selectedDay: number | null = null;

  months: string[] = [
    'I', 'II', 'III', 'IV', 'V', 'VI',
    'VII', 'VIII', 'IX', 'X', 'XI', 'XII'
  ]
  days: string[] = [
    'SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT'
  ]

  constructor() {
    this.updateCalendar();
  }

  updateCalendar(): void {
    const year = this.currentDate.getFullYear();
    const month = this.currentDate.getMonth();
    this.currentMonth = this.months[month];
    this.currentYear = year;

    const firstDay = new Date(year, month, 1).getDay();
    const daysInThisMonth = new Date(year, month + 1, 0).getDate();

    this.daysInMonth = Array(firstDay).fill(0);
    for (let i = 1; i <= daysInThisMonth; i++) {
      this.daysInMonth.push(i);
    }
    while (this.daysInMonth.length < 42) {
      this.daysInMonth.push(0);
    }
  }

  gotoPreviousMonth(): void {
    this.selectedDay = null;
    this.currentDate = new Date(this.currentDate.getFullYear(), this.currentDate.getMonth() - 1);
    this.updateCalendar();
  }

  gotoNextMonth(): void {
    this.selectedDay = null;
    this.currentDate = new Date(this.currentDate.getFullYear(), this.currentDate.getMonth() + 1);
    this.updateCalendar();
  }

  clickDay(day: number): void {
    if (this.selectedDay === day) {
      this.selectedDay = null
      this.selectDate.emit(null)
    }
    else {
      this.selectedDay = day;
      const date = new Date(this.currentDate.getFullYear(), this.currentDate.getMonth(), day);
      this.selectDate.emit(date)
    }
  }
}

