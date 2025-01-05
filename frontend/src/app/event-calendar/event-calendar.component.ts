import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TranslateModule } from '@ngx-translate/core';
import { Router } from '@angular/router';
import { TopBarComponent } from '../bars/top-bar/top-bar.component';
import { CalendarComponent } from '../component/calendar/calendar.component';
import { OverlayNewEventComponent } from '../overlays/overlay-new-event/overlay-new-event.component';
import { GroupInfo } from '../interfaces';
import { SessionStateServiceService } from '../services/session-state/session-state-service.service';

@Component({
  selector: 'app-event-calendar',
  standalone: true,
  imports: [CommonModule, TranslateModule, CalendarComponent, TopBarComponent, OverlayNewEventComponent],
  templateUrl: './event-calendar.component.html',
  styleUrl: './event-calendar.component.css'
})
export class EventCalendarComponent {
  group!: GroupInfo
  selectedDate: Date | null = null
  visibleOverlayEvent = false

  events = [{name: "Koncert Wigilijny", date: new Date('2024-12-24')}] //mock

  constructor(private router: Router, private state: SessionStateServiceService) {
    this.state.currentGroup.subscribe((group) => {
      this.group = group;
    });
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

  isSameDate(date1: Date | null, date2: Date): boolean {
    if (!date1) return false;
    return date1.toDateString() === date2.toDateString();
  }
}
