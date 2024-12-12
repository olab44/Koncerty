import { Component } from '@angular/core';
import { TopBarComponent } from '../top-bar/top-bar.component';

@Component({
  selector: 'app-event-calendar',
  standalone: true,
  imports: [TopBarComponent],
  templateUrl: './event-calendar.component.html',
  styleUrl: './event-calendar.component.css'
})
export class EventCalendarComponent {

}
