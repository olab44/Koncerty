import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TranslateModule } from '@ngx-translate/core';
import { Router } from '@angular/router';
import { TopBarComponent } from '../bars/top-bar.component';
import { OverlayNewEventComponent } from '../overlays/overlay-new-event/overlay-new-event.component';

@Component({
  selector: 'app-event-calendar',
  standalone: true,
  imports: [CommonModule, TranslateModule, TopBarComponent, OverlayNewEventComponent],
  templateUrl: './event-calendar.component.html',
  styleUrl: './event-calendar.component.css'
})
export class EventCalendarComponent {
  group: any
  visibleOverlayEvent = false

  events = [{name: "Koncert Wigilijny"}]

  constructor(private router: Router) {
    this.group = history.state.group;
  }

  gotoEvent(event: any) {
    const group = this.group
    this.router.navigate(['/group/event'], {state: {group, event}});
  }

  toggleOverlayEvent(): void {
    this.visibleOverlayEvent = !this.visibleOverlayEvent
  }
}
