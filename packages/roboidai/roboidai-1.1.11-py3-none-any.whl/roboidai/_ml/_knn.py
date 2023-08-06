# Part of the ROBOID project - http://hamster.school
# Copyright (C) 2016 Kwang-Hyun Park (akaii@kw.ac.kr)
# 
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
# 
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General
# Public License along with this library; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330,
# Boston, MA  02111-1307  USA

import base64, codecs
magic = 'IyBQYXJ0IG9mIHRoZSBST0JPSUQgcHJvamVjdCAtIGh0dHA6Ly9oYW1zdGVyLnNjaG9vbAojIENvcHlyaWdodCAoQykgMjAxNiBLd2FuZy1IeXVuIFBhcmsgKGFrYWlpQGt3LmFjLmtyKQojIAojIFRoaXMgbGlicmFyeSBpcyBmcmVlIHNvZnR3YXJlOyB5b3UgY2FuIHJlZGlzdHJpYnV0ZSBpdCBhbmQvb3IKIyBtb2RpZnkgaXQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBHTlUgTGVzc2VyIEdlbmVyYWwgUHVibGljCiMgTGljZW5zZSBhcyBwdWJsaXNoZWQgYnkgdGhlIEZyZWUgU29mdHdhcmUgRm91bmRhdGlvbjsgZWl0aGVyCiMgdmVyc2lvbiAyLjEgb2YgdGhlIExpY2Vuc2UsIG9yIChhdCB5b3VyIG9wdGlvbikgYW55IGxhdGVyIHZlcnNpb24uCiMgCiMgVG'
love = 'ucplOfnJWlLKW5VTymVTEcp3ElnJW1qTIxVTyhVUEbMFObo3OyVUEbLKDtnKDtq2yfoPOvMFO1p2IzqJjfPvZtLaI0VSqWIRuCIIDtDH5MVSqOHyWOGyEMBlO3nKEbo3I0VTI2MJ4tqTuyVTygpTkcMJDtq2SlpzShqUxto2LXVlOAEIWQFRSBIRSPFHkWISxto3VtExyHGxIGHlOTG1VtDFODDIWHFHAIGRSFVSOIHyOCH0HhVPOGMJHtqTuyVRqBIDbwVRkyp3AypvOUMJ5ypzSfVSO1LzkcLlOZnJAyoaAyVTMipvOgo3WyVTEyqTScoUZhPvZtPvZtJJ91VUAbo3IfMPObLKMyVUWyL2IcqzIxVTRtL29jrFOiMvO0nTHtE05IVRkyp3AypvOUMJ5ypzSfPvZtHUIvoTywVRkcL2Ihp2HtLJkiozptq2y0nPO0nTymVTkcLaWupax7VTyzVT5iqPjtq3WcqTHtqT8tqTuyPvZt'
god = 'RnJlZSBTb2Z0d2FyZSBGb3VuZGF0aW9uLCBJbmMuLCA1OSBUZW1wbGUgUGxhY2UsIFN1aXRlIDMzMCwKIyBCb3N0b24sIE1BICAwMjExMS0xMzA3ICBVU0EKCgpmcm9tIHNrbGVhcm4ubmVpZ2hib3JzIGltcG9ydCBLTmVpZ2hib3JzQ2xhc3NpZmllcgppbXBvcnQgbnVtcHkgYXMgbnAKCgpjbGFzcyBLbm46CiAgICBkZWYgX19pbml0X18oc2VsZiwgbmVpZ2hib3JzPTMpOgogICAgICAgIHNlbGYuX21vZGVsID0gS05laWdoYm9yc0NsYXNzaWZpZXIobl9uZWlnaGJvcnM9bmVpZ2hib3JzKQogICAgICAgIHNlbGYuY2xlYXIoKQoKICAgIGRlZiBjbGVhcihzZWxmKToKICAgICAgICBzZWxmLl9sYWJlbHMgPSBbXQogICAgICAgIHNlbGYuX3RyYWluX2RhdGEgPS'
destiny = 'OoKDbXVPNtVTEyMvOfo2SxK3ElLJyhXUAyoTLfVTkuLzIfYPOznJkypTS0nPx6PvNtVPNtVPNtMTS0LFN9VT5jYzkiLJE0rUDbMzyfMKOuqTtfVTEyoTygnKEypw0aYPpcPvNtVPNtVPNtp2IfMv5sqUWunJ5sMTS0LF5yrUEyozDbMTS0LFxXVPNtVPNtVPOfLJWyoUZtCFOooTSvMJkqVPbtMTS0LF5mnTSjMIfjKDbtVPNtVPNtVUAyoTLhK2kuLzIfpl5yrUEyozDboTSvMJkmXDbXVPNtVTEyMvO0pzScovumMJkzXGbXVPNtVPNtVPOmMJkzYy9go2EyoP5znKDbp2IfMv5sqUWunJ5sMTS0LFjtp2IfMv5soTSvMJkmXDbXVPNtVTEyMvOjpzIxnJA0XUAyoTLfVUMyL3Eipvx6PvNtVPNtVPNtpzI0qKWhVUAyoTLhK21iMTIfYaOlMJEcL3DbJ3MyL3Eipy0cJmOqPt=='
joy = '\x72\x6f\x74\x31\x33'
trust = eval('\x6d\x61\x67\x69\x63') + eval('\x63\x6f\x64\x65\x63\x73\x2e\x64\x65\x63\x6f\x64\x65\x28\x6c\x6f\x76\x65\x2c\x20\x6a\x6f\x79\x29') + eval('\x67\x6f\x64') + eval('\x63\x6f\x64\x65\x63\x73\x2e\x64\x65\x63\x6f\x64\x65\x28\x64\x65\x73\x74\x69\x6e\x79\x2c\x20\x6a\x6f\x79\x29')
eval(compile(base64.b64decode(eval('\x74\x72\x75\x73\x74')),'<string>','exec'))