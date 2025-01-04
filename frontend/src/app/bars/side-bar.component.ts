import { Component, Input } from '@angular/core';
import { GroupInfo } from '../interfaces';
import { TranslateModule } from '@ngx-translate/core';

@Component({
  selector: 'app-side-bar',
  standalone: true,
  imports: [TranslateModule],
  templateUrl: './side-bar.component.html',
  styleUrl: './side-bar.component.css'
})
export class SideBarComponent {
  @Input() isEditAvailable: boolean = false;
  @Input() group: GroupInfo | null = null;
}
