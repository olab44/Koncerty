import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms'
import { TranslateModule } from '@ngx-translate/core';
import { GroupInfo } from '../interfaces';

@Component({
  selector: 'app-side-bar',
  standalone: true,
  imports: [CommonModule, FormsModule, TranslateModule],
  templateUrl: './side-bar.component.html',
  styleUrl: './side-bar.component.css'
})
export class SideBarComponent {
  @Input() isEditAvailable: boolean = false;
  @Input() group: GroupInfo = {group_id: -1, group_name: "", role: ""};
  editMessage = ""
  saveGroupInfo() {
    this.editMessage = "Group info saved."
    setTimeout(() => {
      this.editMessage = '';
    }, 5000);
  }
}
