import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { TranslateModule } from '@ngx-translate/core';
import { TopBarComponent } from '../bars/top-bar/top-bar.component';
import { SideBarComponent } from '../bars/side-bar/side-bar.component';
import { GroupInfo, UserInfo } from '../interfaces';
import { SessionStateService } from '../services/session-state/session-state.service';
import { BackendService } from '../services/backend-connection/backend.service';

@Component({
  selector: 'app-group-control',
  standalone: true,
  imports: [CommonModule, FormsModule, TranslateModule, TopBarComponent, SideBarComponent],
  templateUrl: './group-control.component.html',
  styleUrl: './group-control.component.css'
})
export class GroupControlComponent {
  group!: GroupInfo
  newSubgroup = {parent_group: -1, name: '', extra_info: '', members: []}
  group_members: UserInfo[] = []

  constructor(private backend: BackendService, private state: SessionStateService) {
    this.state.currentGroup.subscribe((group) => {
      this.group = group;
      this.newSubgroup.parent_group = group.group_id
    });
    this.getUsers()
  }

  getUsers() {
    this.backend.getUsers(this.group.group_id).subscribe({
      next: (res) => {
        console.log(res)
      },
      error: (e) => {
        console.log(e);
      },
    })
  }

  createSubgroup() {
    this.backend.postRequest('groups/createSubgroup', this.newSubgroup).subscribe({
      next: (res) => {
        console.log(res)
      },
      error: (e) => {
        console.log(e);
      },
    });
  }

  deleteSubgroup(id: number) {
    this.group.subgroups = this.group.subgroups?.filter((subgroup) => subgroup.subgroup_id !== id)
    this.backend.postRequest('groups/deleteSubgroup', {group_id: id}).subscribe({
      next: (res) => {
        console.log(res)
      },
      error: (e) => {
        console.log(e);
      },
    });
  }

  inviteMember(email: string) {
    // send mail with invitation code
  }

  removeGroupMember(id: number) {
    this.group_members = this.group_members.filter((member) => member.id !== id);
    this.getUsers()
  }

  updateMemberRole(member: any) {
    console.log(`Updated role for ${member.email}: ${member.role}`);
  }
}
