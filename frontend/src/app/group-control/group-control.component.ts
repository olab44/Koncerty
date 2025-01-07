import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { TranslateModule } from '@ngx-translate/core';
import { TopBarComponent } from '../bars/top-bar/top-bar.component';
import { SideBarComponent } from '../bars/side-bar/side-bar.component';
import { GroupInfo, SubgroupInfo, UserInfo } from '../interfaces';
import { SessionStateService } from '../services/session-state/session-state.service';
import { BackendService } from '../services/backend-connection/backend.service';
import { FilterPipe } from '../pipe/filter.pipe';

@Component({
  selector: 'app-group-control',
  standalone: true,
  imports: [CommonModule, FormsModule, TranslateModule, TopBarComponent, SideBarComponent, FilterPipe],
  templateUrl: './group-control.component.html',
  styleUrl: './group-control.component.css'
})
export class GroupControlComponent {
  group!: GroupInfo
  newSubgroup = {parent_group: -1, name: '', extra_info: '', members: []}
  group_members: UserInfo[] = []
  subgroup_members: UserInfo[] = []
  viewed_subgroup_id: number = 0
  searchPhrase: string = ""
  filterMode: string = "email"
  inviteEmail: string = ""
  addEmail: string = ""

  constructor(private backend: BackendService, private state: SessionStateService) {
    this.state.currentGroup.subscribe((group) => {
      this.group = group;
      this.newSubgroup.parent_group = group.group_id
    })
    this.getGroupUsers()
  }

  getGroupUsers() {
    this.backend.getUsers(this.group.group_id).subscribe({
      next: (res) => {
        this.group_members = res
      },
      error: (e) => {
        console.log(e);
      },
    })
  }
  selectSubgroup(group_id: number) {
    if (this.viewed_subgroup_id === group_id) {
      this.viewed_subgroup_id = 0
      this.subgroup_members = []
    }
    else {
      this.viewed_subgroup_id = group_id
      this.backend.getUsers(group_id).subscribe({
        next: (res) => {
          this.subgroup_members = res
        },
        error: (e) => {
          console.log(e);
        },
      })
    }
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

  removeGroupMember(group_id: number, user_email: string) {
    this.backend.deleteRequest('removeMember', {group_id, user_email}).subscribe({
      next: (res) => {
        if (group_id === this.group.group_id) {this.group_members = this.group_members.filter(member => member.email !== user_email)}
        else {this.subgroup_members = this.group_members.filter(member => member.email !== user_email)}
      },
      error: (e) => {
        console.log(e);
      },
    });
  }

  updateMemberRole(member: UserInfo) {
    console.log(`Updated role for ${member.email}: ${member.role}`);
    this.backend.postRequest('changeRole', {group_id: this.group.group_id, user_email: member.email,  new_role: member.role}).subscribe({
      next: (res) => {},
      error: (e) => {
        if (e.error.detail === "Cannot change role. At least one 'Kapelmistrz' roles must remain in the group.") {member.role = "Kapelmistrz"}
        console.log(e);
      },
    });
  }

  inviteMember(email: string) {
    // send mail with invitation code
  }

  addMember(user: UserInfo, group_id: number) {
    const user_id = user.id
    this.backend.postRequest('addMember', {user_id, group_id}).subscribe({
      next: (res) => {
        if (group_id === this.group.group_id) {this.group_members.push(user)}
        else {this.subgroup_members.push(user)}
      },
      error: (e) => {
        console.log(e);
      },
    });
  }
}
