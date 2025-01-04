import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TranslateModule } from '@ngx-translate/core';
import { Router } from '@angular/router';
import { BackendService } from '../services/backend-connection/backend.service';
import { TopBarComponent } from '../bars/top-bar.component';
import { CalendarComponent } from '../component/calendar/calendar.component';
import { OverlayNewEventComponent } from '../overlays/overlay-new-event/overlay-new-event.component';
import { EventInfo, GroupInfo } from '../interfaces';

@Component({
  selector: 'app-event-calendar',
  standalone: true,
  imports: [CommonModule, TranslateModule, CalendarComponent, TopBarComponent, OverlayNewEventComponent],
  templateUrl: './event-calendar.component.html',
  styleUrl: './event-calendar.component.css'
})
export class EventCalendarComponent {
  group: GroupInfo
  events: EventInfo[] = []
  selectedDate: Date | null = null
  visibleOverlayEvent: boolean = false

  constructor(private router: Router, private backend: BackendService) {
    this.group = history.state.group;
    this.backend.getEvents().subscribe({
      next: (res) => {
        this.events = res
      },
      error: (e) => {
        console.log(e);
      },
    })
  }

  selectDate(date: Date | null): void {
    this.selectedDate = date
  }

  gotoEvent(event: any) {
    const group = this.group
    this.router.navigate(['/group/event'], {state: {group, event}});
  }

  toggleOverlayEvent(): void {
    this.visibleOverlayEvent = !this.visibleOverlayEvent
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
