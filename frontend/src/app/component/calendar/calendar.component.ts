import { Component, EventEmitter, Input, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TranslateModule } from '@ngx-translate/core';
import { EventInfo } from '../../interfaces';

@Component({
  selector: 'app-calendar',
  standalone: true,
  imports: [CommonModule, TranslateModule],
  templateUrl: './calendar.component.html',
  styleUrl: './calendar.component.css'
})
export class CalendarComponent {
  @Output() selectDate = new EventEmitter<Date | null>()
  @Input() events!: EventInfo[];

  selectedDate: Date = new Date();
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
    const year = this.selectedDate.getFullYear();
    const month = this.selectedDate.getMonth();
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
    this.selectedDate = new Date(this.selectedDate.getFullYear(), this.selectedDate.getMonth() - 1);
    this.updateCalendar();
  }

  gotoNextMonth(): void {
    this.selectedDay = null;
    this.selectedDate = new Date(this.selectedDate.getFullYear(), this.selectedDate.getMonth() + 1);
    this.updateCalendar();
  }

  clickDay(day: number): void {
    if (this.selectedDay === day) {
      this.selectedDay = null
      this.selectDate.emit(null)
    }
    else {
      this.selectedDay = day;
      const date = new Date(this.selectedDate.getFullYear(), this.selectedDate.getMonth(), day);
      this.selectDate.emit(date)
    }
  }

  isEventPlanned(day: number | null): boolean {
    if (!day) return false;
    const date = new Date(this.selectedDate.getFullYear(), this.selectedDate.getMonth(), day);
    return this.events.some(event =>  this.isAtDate(date, event.date_start, event.date_end))
  }

  isAtDate(date_selected: Date | null, date_start: string, date_end: string): boolean {
    if (!date_selected) return false;
    const start_date = new Date(date_start)
    const end_date = new Date(date_end)
    start_date.setHours(0, 0, 0, 0);  end_date.setHours(0, 0, 0, 0);
    const after_start = start_date <= date_selected
    const before_end = date_selected <= end_date
    return after_start && before_end;
  }
}
