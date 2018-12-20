# -*- coding: utf-8 -*-
import sys


def get_deployments_list():
    application_deployments_list = []
    application_deployments = AdminConfig.list('ApplicationDeployment').split('\n')
    for application_deployment in application_deployments:
        application_deployment_dict = {}
        application_deployment_dict['object'] = application_deployment
        application_deployment_dict['object_name'] = str(AdminConfig.getObjectName(application_deployment))
        if not application_deployment_dict['object_name']:
            continue
        application_deployment_dict['app_name'] = (AdminConfig.showAttribute(application_deployment, 'binariesURL').split('/')[-1]).split('.ear')[0]
        if application_deployment_dict['app_name'].endswith('}'):
            continue
        for deployment_target in AdminConfig.list('DeploymentTargetMapping', application_deployment).split('\n'):
            if deployment_target:
                app_state = AdminConfig.showAttribute(deployment_target, 'enable')
                if app_state:
                    if 'enabled' in application_deployment_dict.keys():
                        if application_deployment_dict['enabled'] == 'false':
                            application_deployment_dict['enabled'] = app_state
                    else:
                        application_deployment_dict['enabled'] = app_state
        application_deployments_list.append(application_deployment_dict)
    return application_deployments_list


def get_stopped_apps(application_deployments_list):
    stopped_apps = []
    app_list = AdminApp.list().split('\n')
    for app in application_deployments_list:
        if app['app_name'] in app_list:
            mbean = AdminControl.queryNames('type=Application,name=%s,*' % app['app_name'])
            if mbean:
                pass
            else:
                if app['enabled'] == 'true':
                    stopped_apps.append(app['app_name'])
    return stopped_apps


def main():
    rc = 0
    application_deployments_list = get_deployments_list()
    stopped_apps = get_stopped_apps(application_deployments_list)
    if stopped_apps:
        for stopped_app in stopped_apps:
            print("ansible WARNING!!! Appication '%s' not running!" % stopped_app)
            rc = 1
    return rc


sys.exit(main())
