import { Component } from '@angular/core';
import { TopBarComponent } from '../top-bar/top-bar.component';

@Component({
  selector: 'app-event-details',
  standalone: true,
  imports: [TopBarComponent],
  templateUrl: './event-details.component.html',
  styleUrl: './event-details.component.css'
})
export class EventDetailsComponent {

}
