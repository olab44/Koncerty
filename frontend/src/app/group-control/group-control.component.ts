import { Component } from '@angular/core';
import { TopBarComponent } from '../bars/top-bar.component';

@Component({
  selector: 'app-group-control',
  standalone: true,
  imports: [TopBarComponent],
  templateUrl: './group-control.component.html',
  styleUrl: './group-control.component.css'
})
export class GroupControlComponent {

}
