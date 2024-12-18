import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TranslateModule } from '@ngx-translate/core';
import { Router } from '@angular/router';
import { TopBarComponent } from '../bars/top-bar.component';
import { CalendarComponent } from '../component/calendar/calendar.component';
import { OverlayNewEventComponent } from '../overlays/overlay-new-event/overlay-new-event.component';

@Component({
  selector: 'app-event-calendar',
  standalone: true,
  imports: [CommonModule, TranslateModule, CalendarComponent, TopBarComponent, OverlayNewEventComponent],
  templateUrl: './event-calendar.component.html',
  styleUrl: './event-calendar.component.css'
})
export class EventCalendarComponent {
  group: any
  selectedDate: Date | null = null
  visibleOverlayEvent = false

  events = [{name: "Koncert Wigilijny"}]

  constructor(private router: Router) {
    this.group = history.state.group;
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
}
